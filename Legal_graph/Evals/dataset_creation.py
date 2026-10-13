from dotenv import load_dotenv
load_dotenv()
import json
from langsmith import Client
import os

# loading the eval dataset
with open('Legal_graph\\Evals\\datasets\\eval_dataset.json', 'r') as f:
    datasets = json.load(f)

# print(dataset)
client = Client()
dataset_name = os.environ['LANGSMITH_PROJECT_NAME']

dataset = client.create_dataset(dataset_name=dataset_name,
                                description=(
        "Golden evaluation dataset for the AI Legal Assistant. "
        "Evaluates legal answer quality and RAG performance."
    ))

for record in datasets:
    # print(record)
    client.create_example(
        dataset_id=dataset.id,
        inputs={
            "question": record["input"],
        },
        outputs={
            "ground_truth": record["output"],
            "reference_context": record["context"],
        },
        metadata={
            "record_id": record["id"],
            "case_name": record["case_name"],
            "citation": record["citation"],
            "judgment_date": record["judgment_date"],
            "statutes": record["statutes"],
            "source_pdf": record["source_pdf"],
        },
        split="test",
    )