from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from dotenv import load_dotenv
import json
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
import os
load_dotenv()

client = QdrantClient(url="http://localhost:6333")
# client.create_collection(
#     collection_name="LegalDocs_collection",
#     vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
#     sparse_vectors_config={
#         "sparse": SparseVectorParams(index=models.SparseIndexParams(on_disk=False))
#     },

# )

embeddings = OpenAIEmbeddings(
    model="baai/bge-m3",
    openai_api_key=os.environ.get("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    check_embedding_ctx_length=False,
)

sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

qdrant = QdrantVectorStore(
    client=client,
    collection_name="LegalDocs_collection",
    embedding=embeddings,
    sparse_embedding=sparse_embeddings,
    retrieval_mode=RetrievalMode.HYBRID,
    sparse_vector_name="sparse",
)


with open('C:\\Users\\soodm\\Desktop\\AI Legal Assitant V2\\Legal_graph\\data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


docs = []
for item in data if isinstance(data, list) else [data]:
    if isinstance(item, dict):
        text = item.get("content", "")
        metadata = item.get("metadata", {})
    else:
        text = str(item)
        metadata = {}
    docs.append(Document(page_content=text, metadata=metadata))

print(f"Loaded {len(docs)} documents")

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False, 

)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=300,
    length_function=len,
    separators=["\n\n", "\n", ".", " "] 
)

all_docs = []
for doc in docs:
    markdown_chunks = markdown_splitter.split_text(doc.page_content)

    # e.g. "Abdul_Nassar_vs_State_Of_Kerala_on_7_January_2025_1.PDF" -> "Abdul Nassar vs State Of Kerala on 7 January 2025"
    raw_source = doc.metadata.get("source", "")
    case_name = (
        raw_source
        .replace(".PDF", "")
        .replace(".pdf", "")
        .replace("_", " ")
        .strip()
    )

    for markdown_doc in markdown_chunks:
        text_chunks = text_splitter.split_text(markdown_doc.page_content)

        for i, chunk in enumerate(text_chunks):
            metadata = doc.metadata.copy()
            metadata.update(markdown_doc.metadata)
            metadata["chunk_index"] = i
            metadata["source"] = raw_source
            metadata["case_name"] = case_name  # enables case-name filtering in Qdrant

            # Build a pipe-separated header breadcrumb (e.g. "Judgment | Facts | Background")
            header_breadcrumb = " | ".join(
                value
                for key, value in sorted(markdown_doc.metadata.items())
                if key.startswith("Header") and value
            )

            # Prepend case identity and section breadcrumb so every chunk is self-contained
            parts = [f"Case: {case_name}"]
            if header_breadcrumb:
                parts.append(header_breadcrumb)
            parts.append(chunk)
            enhanced_chunk = "\n\n".join(parts)

            all_docs.append(Document(page_content=enhanced_chunk, metadata=metadata))

qdrant.add_documents(documents=all_docs, batch_size=16)