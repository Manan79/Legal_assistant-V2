import os
import sys
import asyncio
import time
from langsmith import Client

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from Legal_graph.Evals.Accuracy_eval import accuracy
from Legal_graph.Evals.Correctness_eval import correctness
from Legal_graph.Evals.relevancy_eval import relevancy
from Legal_graph.Evals.Faithfullness_eval import faithfulness
from Legal_graph.Agent.react_agent import main_react_agent
# from Legal_graph.tools.vectorstore_tool import retireved_docs


def target(input: dict)-> dict:
    result = asyncio.run(main_react_agent(input['question']))
    return {
        "answer": result["answer"],
        "retrieved_context": result["context"],
    }



client = Client()
start = time.time()
experiments = client.evaluate(
    target,
    data="Legal_AI_Evals_V2",
    evaluators=[
        accuracy,
        correctness,
        relevancy,
        faithfulness,
    ],
    experiment_prefix="Qdrant_rag_V2",
    metadata={
        "version": "Legal_AI_Assitant_V2",
        "evaluation_rubric": "Calibrated_V3",
    },
)

end = time.time() - start
print("Total time taken ", end)

print(f"Experiment finished.")
