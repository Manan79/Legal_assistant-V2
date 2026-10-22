from langchain.tools import tool
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import os
import re
from bs4 import BeautifulSoup

load_dotenv()
embeddings = OpenAIEmbeddings(
    model="baai/bge-m3",
    openai_api_key=os.environ.get("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    check_embedding_ctx_length=False,
)

sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

client = QdrantClient(
    url=os.environ["QDRANT_URL"],
    api_key=os.environ["QDRANT_API_KEY"],
)



vector_store = QdrantVectorStore(
    client=client,
    collection_name="LegalDocs",
    embedding=embeddings,
    sparse_embedding=sparse_embeddings,
    retrieval_mode=RetrievalMode.HYBRID,
    sparse_vector_name="sparse",
)



def clean_legal_text(text: str) -> str:
    # Remove HTML tags and convert entities
    text = BeautifulSoup(text, "html.parser").get_text(" ")

    # Remove Markdown formatting
    text = re.sub(r"[*#`|]", " ", text)

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)

    # Remove page artifacts and extra whitespace
    text = re.sub(r"\b\d{2}:\d{2}:\d{2}\s+IST Reason:", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def retrieve_documents(query: str, k: int = 5, search_type: str = "mmr") -> str:
    """Core retrieval logic from the vector database.

    Args:
        query: The search query string.
        k: Number of retrieved chunks.
        search_type: Retrieval strategy ("similarity" or "mmr" for Maximal Marginal Relevance).
    """
    try:
        if search_type.lower() == "mmr":
            # MMR balances relevance and diversity to avoid redundant chunks from the same judgment section
            retriever = vector_store.as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": k,
                    "fetch_k": k * 4,  # Fetch a larger pool of candidates before diversification
                    "lambda_mult": 0.5  # 0.5 balances relevance and diversity
                }
            )
            docs = retriever.invoke(query)
        else:
            # Standard similarity / hybrid search
            docs = vector_store.similarity_search(query, k=k)

        if not docs:
            return "No relevant legal documents found for the query."

        context = "\n\n".join(
            clean_legal_text(doc.page_content)
            for doc in docs
        )
        print("Vectorstore responded")
        return context
    except Exception as e:
        return f"Error retrieving results from vector store: {str(e)}"


@tool
def get_retrieved_results(query: str, k: int = 4) -> str:
    """This tool is used for retrieving results from the vector database using MMR for diverse legal context.
    Args:
        query: The search query string.
        k: Number of retrieved chunks.
    """
    return retrieve_documents(query, k=k, search_type="mmr")


if __name__ == "__main__":
    test_query = "Abdul Nassar vs State Of Kerala"
    print(f"Testing retriever with query: '{test_query}'")
    res = retrieve_documents(query=test_query, k=3)
    print("Result snippet:\n", res)





# Example: filter by case name using metadata (use this when you know the case)
# results = vector_store.similarity_search_with_score(
#     query="what is the Nirmiti Developers case",
#     k=6,
#     filter=models.Filter(
#         should=[
#             models.FieldCondition(
#                 key="metadata.case_name",
#                 match=models.MatchText(text="Nirmiti"),
#             )
#         ]
#     ),
# 
# for doc, score in results:
#     print(f"* [SIM={score:.3f}]")
#     print("---" * 30)
#     print(f" Page Content: {doc.page_content}")
#     print("---" * 30)
#     print(f" Metadata: {doc.metadata}")
