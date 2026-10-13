from dotenv import load_dotenv
load_dotenv()
from langchain_openrouter import ChatOpenRouter
from langchain.chat_models import init_chat_model
from typing import TypedDict, Annotated
import os

Faithfullness_eval_prompt = """
You are evaluating whether the material claims in a legal answer are supported by the supplied evidence.

Check the answer's material factual and legal claims against the evidence. A claim may be supported by a faithful paraphrase or a clear implication; exact wording is not required. Do not demand that every sentence be quoted. Penalize unsupported material claims and claims that contradict the evidence, with greater penalties for central conclusions than peripheral details. If the evidence is empty, do not assume the answer is supported.

Assign one score from 0.0 to 1.0:
- 1.0: All material claims are supported; no meaningful contradiction.
- 0.0: The answer is largely unsupported, contradicted, or there is no evidence to assess it against.
Use intermediate values when warranted. Briefly name the most important unsupported or contradicted claim, if any.
"""

class EvaluationResult(TypedDict):
    score: Annotated[float, "Score from 0 to 1"]
    explanation: Annotated[str, ..., "Explain the reasoning behind your scoring"]

model = ChatOpenRouter(model=os.environ['FAST_MODEL']).with_structured_output(
    EvaluationResult, method="json_schema", strict=True
)
# print(model.invoke("Hi, can you tell me your name ?"))
def faithfulness(inputs: dict, outputs: dict) -> dict:
    retrieved_context = outputs.get("retrieved_context")
    if retrieved_context is None:
        retrieved_context = outputs.get("context")
    if retrieved_context is None:
        raise KeyError(
            "Faithfulness evaluator requires 'retrieved_context' or 'context' "
            "in evaluator outputs."
        )

    answer = f"""
    Question: {inputs['question']}
    Retrieved context: {retrieved_context}
    llm response: {outputs['answer']}
    """

    grade = model.invoke([
        {"role": "system", "content": Faithfullness_eval_prompt},
        {"role": "user", "content": answer}
    ])

    return {
        "key": "faithfulness",
        "score": grade["score"],
        "comment": grade["explanation"],
    }
