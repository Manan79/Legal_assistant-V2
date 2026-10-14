import os
import sys
import asyncio

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from langchain.agents import create_agent
from Legal_graph.Agent.models import openrouter_model, openai_model
from Legal_graph.Prompts.System_prompt import (
    LEGAL_SYSTEM_PROMPT_V1,
    LEGAL_SYSTEM_PROMPT_V2,
    LEGAL_SYSTEM_PROMPT_V3,
)
from Legal_graph.tools.vectorstore_tool import get_retrieved_results
from Legal_graph.tools.websearch_tool import websearch
from langchain_google_genai import ChatGoogleGenerativeAI
from Legal_graph.Gaurdrails.gaurdrails import rails, parse_nemo_response


# ── Prompt version selection (for evals) ─────────────────────────────────────

PROMPT_VERSIONS = {
    "v1": LEGAL_SYSTEM_PROMPT_V1,
    "v2": LEGAL_SYSTEM_PROMPT_V2,
    "v3": LEGAL_SYSTEM_PROMPT_V3,
}


# ── Guardrails gate ─────────────────────────────────────────────────────────

async def check_guardrails(user_message: str):
    """
    Run NeMo Guardrails on the user message.
    Returns (should_continue, response_text).
    - should_continue=True  → query passed, invoke the agent.
    - should_continue=False → blocked or scripted dialog, print response_text.
    """
    try:
        nemo_resp = await rails.generate_async(
            messages=[{"role": "user", "content": user_message}]
        )
        text, blocked, reason, is_dialog, needs_rag = parse_nemo_response(nemo_resp)

        if blocked:
            label = reason or "UNKNOWN"
            return False, f"Blocked ({label}): {text}"

        if is_dialog:
            return False, text

        # QUERY_PASSED or unrecognised → let the agent handle it
        return True, None
    except Exception as e:
        print(f"Guardrails execution error: {e}")
        # Fail open gracefully so FastAPI requests don't return 500
        return True, None


# ── Main ─────────────────────────────────────────────────────────────────────

async def main_react_agent(query: str):
    system_prompt = PROMPT_VERSIONS['v1']

    # Build the ReAct agent
    tools = [get_retrieved_results, websearch]
    agent = create_agent(
        # model_name='deepseek/deepseek-v4.1-flash' , tencent/hy-mt2-30b-a3b
        model= ChatGoogleGenerativeAI(model = 'gemini-3.5-flash-lite'),
        tools=tools,
        system_prompt=system_prompt
        
    )

    # Step 1: Guardrails check
    should_continue, guard_response = await check_guardrails(query)
    print(should_continue , guard_response)
    if not should_continue:
        print("Guardrails invoked")
        # Return the error message instead of nothing
        return {
        "answer": guard_response,
        "context": should_continue
    }

    print("Using System prompt Version 2")
    # Step 2: Invoke the ReAct agent (query passed guardrails)
    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
     # 1. Extract the final answer
    final_answer = response["messages"][-1].content

    # 2. Extract retrieved docs from ToolMessage
    retrieved_contexts = []
    for msg in response["messages"]:
        if getattr(msg, "name", None) == "get_retrieved_results":
            retrieved_contexts.append(str(msg.content))
        elif getattr(msg, "name", None) == "websearch":
            retrieved_contexts.append(str(msg.content))


    # retrieved_context_str = "\n\n".join(retrieved_contexts)

    # Return both so your evals (especially Faithfulness) can use it!
    return {
        "answer": final_answer,
        "context": retrieved_contexts
    }




# async def main_react_agent(query: str):
#     # 1. Execute retrieval programmatically upfront (0 agent turns!)
#     retrieved_results = get_retrieved_results(query=query, k=3)
#     retrieved_context_str = "\n\n".join([str(doc.page_content) for doc, score in retrieved_results])

   
#     prompt = f"Query: {query}\n\nRetrieved Legal Context:\n{retrieved_context_str}"

#     model = openai_model()
#     response = model.invoke([
#         {"role": "system", "content": LEGAL_SYSTEM_PROMPT_V2},
#         {"role": "user", "content": prompt}
#     ])

#     return {
#         "answer": response.content,
#         "context": retrieved_context_str
#     }