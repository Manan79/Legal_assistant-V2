from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from typing import TypedDict, Annotated

Accuracy_eval_prompt = """
You are evaluating the factual accuracy of a legal answer against the supplied reference answer.

Compare material facts, case names, outcomes, legal provisions, dates, figures, and stated reasons. Treat a faithful paraphrase as correct. Do not require identical wording or penalize a concise answer for omitting immaterial detail. Penalize material omissions, unsupported factual additions, and contradictions; do not penalize correct relevant detail merely because it is absent from the reference.

Assign one overall score from 0.0 to 1.0:
- 1.0: Material facts are accurate; no meaningful omission or contradiction.
- 0.75: Mostly accurate; one material detail is omitted or slightly misstated.
- 0.5: Mixed; important facts are right, but a material error or omission remains.
- 0.25: Mostly inaccurate or misses the central result.
- 0.0: Irrelevant, fundamentally contradicted, or materially fabricated.
Use intermediate values when warranted. Score factual alignment only, not style or legal reasoning. Briefly identify the main reason for the score.

Provide your score (0 to 1) and a brief justification explaining the deviations found.
"""

class EvaluationResult(TypedDict):
    score: Annotated[float, "Score from 0 to 1"]
    justification: Annotated[str, "Explain the reasoning behind your scoring"]

model = init_chat_model(model="groq:openai/gpt-oss-120b").with_structured_output(
    EvaluationResult, method="json_schema", strict=True
)

# print(model.invoke("Hii, can you tell me your name ?"))

def accuracy(inputs: dict, reference_outputs: dict, outputs: dict) -> dict:
    answer = f"""
    Question: {inputs['question']}
    ground truth answer: {reference_outputs['ground_truth']}
    llm response: {outputs['answer']}
    """

    grade = model.invoke([
        {"role": "system", "content": Accuracy_eval_prompt},
        {"role": "user", "content": answer}
    ])

    return {
        "key": "accuracy",
        "score": grade["score"],
        "comment": grade["justification"],
    }
