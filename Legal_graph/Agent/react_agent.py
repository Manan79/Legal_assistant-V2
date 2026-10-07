import os
import sys
import asyncio

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from langchain.agents import create_agent
from Legal_graph.Agent.models import openrouter_model
from Legal_graph.Prompts.System_prompt import (
    LEGAL_SYSTEM_PROMPT,
    LEGAL_SYSTEM_PROMPT_V1,
    LEGAL_SYSTEM_PROMPT_V2,
    LEGAL_SYSTEM_PROMPT_V3,
)
from Legal_graph.tools.vectorstore_tool import get_retrieved_results
from Legal_graph.Gaurdrails.gaurdrails import rails, parse_nemo_response


# ── Prompt version selection (for evals) ─────────────────────────────────────

PROMPT_VERSIONS = {
    "v1": LEGAL_SYSTEM_PROMPT_V1,
    "v2": LEGAL_SYSTEM_PROMPT_V2,
    "v3": LEGAL_SYSTEM_PROMPT_V3,
}


def select_prompt_version() -> str:
    """Pick a system prompt version from --prompt-version flag or default."""
    version_key = "v2"  # default
    for i, arg in enumerate(sys.argv):
        if arg == "--prompt-version" and i + 1 < len(sys.argv):
            version_key = sys.argv[i + 1].lower()
    if version_key not in PROMPT_VERSIONS:
        print(f"⚠ Unknown prompt version '{version_key}', using v2.")
        version_key = "v2"
    return PROMPT_VERSIONS[version_key]


# ── Guardrails gate ─────────────────────────────────────────────────────────

async def check_guardrails(user_message: str):
    """
    Run NeMo Guardrails on the user message.
    Returns (should_continue, response_text).
    - should_continue=True  → query passed, invoke the agent.
    - should_continue=False → blocked or scripted dialog, print response_text.
    """
    nemo_resp = await rails.generate_async(
        messages=[{"role": "user", "content": user_message}]
    )
    text, blocked, reason, is_dialog, needs_rag = parse_nemo_response(nemo_resp)

    if blocked:
        label = reason or "UNKNOWN"
        return False, f"⛔ Blocked ({label}): {text}"

    if is_dialog:
        return False, text

    # QUERY_PASSED or unrecognised → let the agent handle it
    return True, None


# ── Main ─────────────────────────────────────────────────────────────────────

async def main():
    # Select prompt version
    system_prompt = select_prompt_version()

    # Build the ReAct agent
    tools = [get_retrieved_results]
    agent = create_agent(
        model=openrouter_model(),
        tools=tools,
        system_prompt=system_prompt,
    )

    # Get user query
    query = input("Enter your legal query: ").strip()
    if not query:
        raise SystemExit("Please enter a legal query.")

    # Step 1: Guardrails check
    should_continue, guard_response = await check_guardrails(query)
    if not should_continue:
        print(guard_response)
        return

    # Step 2: Invoke the ReAct agent (query passed guardrails)
    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())