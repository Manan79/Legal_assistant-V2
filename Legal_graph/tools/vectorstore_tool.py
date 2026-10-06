from langchain.tools import tool
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import os

load_dotenv()
embeddings = OpenAIEmbeddings(
    model="baai/bge-m3",
    openai_api_key=os.environ.get("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    check_embedding_ctx_length=False,
)

sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

client = QdrantClient(url="http://localhost:6333")
vector_store = QdrantVectorStore(
    client=client,
    collection_name="LegalDocs_collection",
    embedding=embeddings,
    sparse_embedding=sparse_embeddings,
    retrieval_mode=RetrievalMode.HYBRID,
    sparse_vector_name="sparse",
)

@tool
async def get_retrieved_results(query: str , k: int = 3):
    """This tools is used for retrieving results from the vectordatabase
    args:
        query,
        k : number of retireved chunks
    """
    results = await vector_store.similarity_search_with_score(
        query= query , k=k,
    )

    return results









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
