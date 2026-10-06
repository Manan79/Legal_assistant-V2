import os
import re
import pymupdf
import pymupdf4llm  # pip install pymupdf4llm

pdf_dir = "../2025"
output_dir = "./processed"

os.makedirs(output_dir, exist_ok=True)


def clean_markdown(text: str) -> str:
    # Remove horizontal rule artifacts (----, ====, etc.)
    text = re.sub(r'^[-=]{4,}\s*$', '', text, flags=re.MULTILINE)
    # Remove standalone page numbers (lines that are only digits)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    # Collapse 3+ consecutive blank lines to 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Strip trailing whitespace from each line
    text = '\n'.join(line.rstrip() for line in text.splitlines())
    return text.strip()


documents = []
for filename in os.listdir(pdf_dir):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        # Extract as Markdown to preserve document structure (headers, clauses, sections)
        md_text = pymupdf4llm.to_markdown(pdf_path)
        # Clean noise artifacts from PDF conversion
        md_text = clean_markdown(md_text)

        documents.append({
            "content": md_text,
            "metadata": {"source": filename}
        })
        print(f"Processed: {filename}")

print(f"\nTotal: {len(documents)} documents")


import json

with open("data.json", "w") as f:
    json.dump(documents, f, indent=4)