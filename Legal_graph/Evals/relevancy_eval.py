from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from typing import TypedDict, Annotated

Relevancy_eval_prompt = """
You are an expert legal evaluator. Your task is to evaluate the relevance of the answer to the user's original query.

Evaluation Criteria:
1. Examine the user's intent in the original query.
2. Determine if the generated answer directly addresses that intent without unnecessary preamble or off-topic information.
3. Assess the utility: Does this answer actually solve the user's problem?

Scoring:
- 1.0: Highly relevant and direct; the user immediately gets what they needed.
- 0.5: Addresses part of the query but may be too vague or verbose.
- 0.0: Irrelevant; fails to address the query or provides incorrect focus.

Provide your score (0 to 1) and a brief justification, explaining whether the answer directly hit the mark.
"""

class Retriever_relevance(TypedDict):
    explanation: Annotated[str, ... ,"Explanation of the relevance of the answer"]
    retrieve_relevance: Annotated[bool, ... ,"Whether the answer is relevant or not"] 

model = init_chat_model(model="groq:openai/gpt-oss-120b").with_structured_output(
    Retriever_relevance, method="json_schema", strict=True
)

def relevancy(inputs: dict , outputs: dict ) -> bool:
    
    answer = f""" 

    Question: {inputs['question']}
    llm response: {outputs['answer']}

    """

    grade = model.invoke([
        {"role": "system", "content": Relevancy_eval_prompt},
        {"role": "user", "content": answer}
    ])

    return{
        "key": "retrieval_relevance",
        "score": int(bool(grade["retrieve_relevance"])),
        "comment": grade["explanation"],
    }
