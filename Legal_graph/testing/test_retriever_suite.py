import os
import sys

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from Legal_graph.tools.vectorstore_tool import retrieve_documents

TEST_QUESTIONS = [
    "Abdul Nassar vs State of Kerala circumstantial evidence capital punishment",
    "Abdul Wahid vs State of Rajasthan eyewitness testimony acquittal",
    "Arbitration and commercial law dispute resolution principles",
    "Service law disciplinary inquiry and principles of natural justice",
    "Human trafficking and constitutional law protections",
    "Insolvency and Bankruptcy Code IBC appeal and limitation",
    "Environmental law and wildlife habitat protection",
    "Narcotic Drugs and Psychotropic Substances Act NDPS principles"
]

def run_retriever_tests():
    print("=" * 60)
    print("RUNNING RETRIEVER TEST SUITE")
    print("=" * 60)

    for i, q in enumerate(TEST_QUESTIONS, 1):
        print(f"\n--- Test Question {i}: {q} ---")
        try:
            result = retrieve_documents(query=q, k=3)
            if "Error" in result or "No relevant" in result:
                print(f"Status: [FAILED or EMPTY]\nMessage: {result}")
            else:
                snippet = result[:300].replace("\n", " ")
                print(f"Status: [SUCCESS] (Retrieved {len(result)} characters)")
                print(f"Snippet: {snippet}...")
        except Exception as e:
            print(f"Status: [EXCEPTION]: {e}")

    print("\n" + "=" * 60)
    print("RETRIEVER TEST SUITE COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    run_retriever_tests()
