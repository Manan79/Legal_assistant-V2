from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from typing import TypedDict, Annotated

Correctness_Eval_prompt = """
You are evaluating the legal reasoning and internal logic of an answer to a legal question, using the reference answer as a guide.

Assess whether the answer's stated legal rule supports its conclusion and whether its reasoning is coherent. Allow reasonable paraphrasing and concise explanations. Do not score factual overlap, writing style, or answer relevance here; those are separate measures. Penalize a legal conclusion that does not follow from the stated rule, a material misapplication of law, or contradictory reasoning.

Assign one score from 0.0 to 1.0:
- 1.0: Sound, coherent reasoning with a conclusion supported by the legal principles.
- 0.75: Sound overall, with a minor gap or nuance missing.
- 0.0: Fundamentally incoherent or contrary to the controlling legal principle.
Use intermediate values when warranted. Briefly explain the decisive reasoning issue.
"""


class Correctness(TypedDict):
    score: Annotated[float, "Score from 0 to 1"]
    explanation: Annotated[str, "Brief explanation of the reasoning score"]

model = init_chat_model(model="groq:openai/gpt-oss-20b").with_structured_output(Correctness, method = "json_schema",
                                                                                 strict = True)

def correctness(inputs: dict, reference_outputs: dict, outputs: dict) -> dict:
    answer = f"""
    Question: {inputs['question']}
    ground truth answer: {reference_outputs['ground_truth']}
    llm response: {outputs['answer']}
    """
    grade = model.invoke([
        {"role": "system", "content": Correctness_Eval_prompt},
        {"role": "user", "content": answer},
    ])

    return {
        "key": "legal_correctness",
        "score": grade["score"],
        "comment": grade["explanation"],
    }