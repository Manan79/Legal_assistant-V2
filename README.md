# ⚖️ Legal AI Assistant V2 — Advanced Agentic Legal Intelligence Platform

An enterprise-grade, production-ready AI Legal Assistant specialized in Indian statutory law, Supreme Court jurisprudence, legal procedure, contract analysis, and regulatory compliance. Powered by **LangGraph ReAct Agents**, **Hybrid Vector Retrieval (Dense + Sparse with MMR)**, **NeMo Guardrails**, and a **FastAPI + Tailwind CSS Web Application**.

---

## 🌟 Key Architecture & Capabilities

```
┌────────────────────────────────────────────────────────────────────────┐
│                        User & Modern Web UI                            │
│           (FastAPI /static -> HTML5 + Tailwind CSS + marked.js)       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP POST /legal_assistant
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        NeMo Guardrails Gateway                         │
│   (PII Detection ── Off-topic Filtering ── Jailbreak Prevention)       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ (If Query Passed)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   LangGraph ReAct Agent (Gemini / GPT)                 │
│         (Reasoning ── Action ── Observation ── Synthesis Loop)         │
└──────────────────┬─────────────────────────────┬───────────────────────┘
                   │                             │
                   ▼                             ▼
┌──────────────────────────────────────┐ ┌───────────────────────────────┐
│        Qdrant Hybrid Vector Store    │ │         Tavily WebSearch      │
│  (BAAI/bge-m3 dense + BM25 sparse)   │ │  (Real-time legal updates)    │
│  (MMR Diversity Reranking k=3-6)     │ └───────────────────────────────┘
└──────────────────────────────────────┘
```

---

## 📂 Exact Project Directory Structure

```text
Legal_AI_Assitant_V2/
├── .env
├── .git
├── .gitignore
├── .python-version
├── .venv/
├── Legal_graph/
│   ├── 2025/                      # Source Supreme Court PDF judgments corpus
│   ├── Agent/
│   │   ├── models.py              # LLM client initialisation (OpenRouter, Azure, OpenAI)
│   │   └── react_agent.py         # Core LangGraph ReAct agent loop & guardrails integration
│   ├── Backend/
│   │   └── main.py                # FastAPI server, CORS middleware, static UI mounting
│   ├── Evals/
│   │   ├── Accuracy_eval.py       # Factual correctness evaluator against ground truth
│   │   ├── Correctness_eval.py    # Legal reasoning soundness & rule-conclusion alignment
│   │   ├── Faithfullness_eval.py  # Evidence support & hallucination penalty evaluator
│   │   ├── datasets/
│   │   │   ├── eval_dataset.json  # Comprehensive evaluation test cases
│   │   │   └── golden_dataset.json# Golden reference answers and source contexts
│   │   ├── dataset_creation.py    # LangSmith dataset ingestion & gold standard loader
│   │   └── relevancy_eval.py      # Query intent & answer relevance evaluator
│   ├── Gaurdrails/
│   │   ├── colang_rules.py        # Colang safety dialogs, PII rules, jailbreak defense
│   │   └── gaurdrails.py          # NeMo Guardrails configuration & custom PII detector
│   ├── Prompts/
│   │   └── System_prompt.py       # Versioned system prompts (V1 Concise, V2 CoT, V3 Production)
│   ├── Vector_Database/
│   │   ├── data.json              # Processed markdown corpus of Supreme Court judgments
│   │   ├── database_creation.py   # Hybrid vector embedding & Qdrant collection builder
│   │   └── pdf_to_texts.py        # PyMuPDF4LLM extraction & artifact cleaning pipeline
│   ├── frontend/
│   │   ├── index.html             # Responsive single-page web app (Tailwind CSS v3)
│   │   ├── script.js              # Application logic, Markdown parsing, context drawers
│   │   └── style.css              # Custom typography, glassmorphism & custom scrollbars
│   ├── testing/
│   │   ├── Eval_testing.py        # LangSmith automated experiment runner
│   │   ├── test_guardrails_script.py # Guardrails test suite
│   │   └── test_retriever_suite.py   # Hybrid retriever validation suite
│   └── tools/
│       ├── vectorstore_tool.py    # Qdrant hybrid search tool with MMR diversification
│       └── websearch_tool.py      # Tavily search tool wrapper for real-time legal news
├── README.md                      # Project documentation
├── Readmes/                       # Detailed component documentation & planning logs
├── main.py                        # Simple entry point
├── pyproject.toml                 # Project metadata & build config
├── requirements.txt               # Python package dependencies
└── uv.lock                        # Dependency lock file
```

---

## 📊 Evaluation Results & LangSmith Experiments

Our automated evaluation pipeline tests the agent across 10 repetitions per configuration on LangSmith (`Legal_AI_Evals_V2`), measuring **Accuracy**, **Faithfulness**, **Legal Correctness**, and **Retrieval Relevance** against golden reference data.

| Experiment | Configuration / Model | Accuracy (AVG) | Faithfulness (AVG) | Legal Correctness (AVG) | Retrieval Relevance (AVG) | P50 Latency | P99 Latency | Error Rate |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#2 (Baseline)** | Qdrant RAG v2 (Default) | 0.40 | 0.55 | 0.47 | 0.90 | 10.97s | 11.88s | 0% |
| **#7** | Qdrant RAG v2 + Azure OpenAI | **0.48** (+0.08) | 0.61 (+0.06) | **0.67** (+0.20) | **1.00** (+0.10) | **7.35s** (-3.61s) | 16.04s | **0%** |
| **#4** | Qdrant RAG v2 + Full Vectorstore | 0.44 (+0.04) | **0.69** (+0.14) | 0.57 (+0.10) | **1.00** (+0.10) | 26.44s | 49.16s | 0% |
| **#3** | Qdrant RAG v2 + WebSearch | 0.38 (-0.03) | **0.82** (+0.27) | 0.69 (+0.22) | **1.00** (+0.10) | 15.72s | 44.48s | 40% |

### Key Evaluation Insights:
- **Experiment #7 (Azure OpenAI Integration)** achieved the best balance of speed (**7.35s P50 latency**) and high legal correctness (**0.67**).
- **Faithfulness** peaked at **0.82** when combining web search with RAG context (Experiment #3), though with higher latency and error rate due to external API calls.
- **Retrieval Relevance** reached a consistent **1.00** across all optimized retriever runs using MMR diversity reranking.

---

## 🧠 1. Agent Architecture & ReAct Loop

The core agent (`Legal_graph/Agent/react_agent.py`) is built using **LangGraph** and implements a **ReAct (Reasoning + Acting)** paradigm:
1. **Guardrails Interception**: Incoming queries are screened by NeMo Guardrails before agent execution.
2. **Reasoning Step**: The model analyzes the legal question and decides whether to invoke retrieval tools or web search.
3. **Tool Execution**: Calls `get_retrieved_results` (vector search) or `websearch`.
4. **Observation & Synthesis**: Synthesizes retrieved judgments, statutes, and provisions into a structured legal brief.

### Model Integration (`Legal_graph/Agent/models.py`)
- Configured to support multi-provider LLMs (**Google Gemini 3.5 Flash Lite**, **OpenAI GPT-4o-mini**, **Azure/Foundry models**, and **OpenRouter**).
- Temperature set to `0.4` for balanced legal precision and explanatory fluency.

---

## 🔍 2. Vector Database & Hybrid Retrieval

Legal documents (Supreme Court judgments, statutes) undergo a rigorous ingestion pipeline:
1. **PDF Extraction (`pdf_to_texts.py`)**: Converted using `pymupdf4llm` to preserve markdown structure (headers, clauses) while cleaning artifacts, horizontal rules, and page numbers.
2. **Hybrid Chunking & Enrichment (`database_creation.py`)**:
   - Markdown header splitting (`#`, `##`, `###`) to respect legal document hierarchy.
   - Recursive character text splitting (chunk size: 2000, overlap: 300).
   - Metadata enrichment: case name extraction, chunk indices, and hierarchical header breadcrumbs.
3. **Qdrant Vector Store (`vectorstore_tool.py`)**:
   - **Dense Embeddings**: `BAAI/bge-m3` via OpenRouter.
   - **Sparse Embeddings**: `Qdrant/bm25` (FastEmbedSparse) for keyword matching.
   - **Retrieval Mode**: Hybrid search (`RetrievalMode.HYBRID`).
   - **MMR Diversification**: Maximal Marginal Relevance (`search_type="mmr"`, `lambda_mult=0.5`, `fetch_k = k * 4`) balances relevance with diverse case perspectives, eliminating redundant chunks from the same judgment section.

---

## 🛠️ 3. Agent Tools

- **`get_retrieved_results(query, k=5)`**: Queries the Qdrant hybrid vector store using MMR retrieval. Cleans HTML/Markdown artifacts and returns rich contextual legal excerpts with source provenance.
- **`websearch(query)`**: Integrates **TavilySearch** to fetch real-time legal updates, recent Supreme Court notifications, and legislative announcements when vector retrieval is insufficient.

---

## 🛡️ 4. NeMo Guardrails & Safety

Implemented via **NeMo Guardrails** (`Legal_graph/Gaurdrails/gaurdrails.py` and `colang_rules.py`):
- **PII Detection**: Automatically scans input messages for emails, phone numbers, SSNs, API keys, and credit cards using regex action `detect_pii`.
- **Off-Topic Blocking**: Refuses non-legal queries (cooking, coding, weather, jokes, general trivia) with professional redirection.
- **Jailbreak Protection**: Defends against prompt injection, role override, and DAN ("Do Anything Now") attacks.
- **Confidential Data Filtering**: Blocks queries requesting internal HR records, employee salaries, or performance reviews.
- **Scripted Greetings**: Handles casual greetings instantly without wasting LLM token budget.

---

## 🖥️ 5. FastAPI Backend & Modern Frontend UI

### Backend (`Legal_graph/Backend/main.py`)
- Built with **FastAPI** featuring CORS middleware, static file mounting (`/static`), and OpenAPI documentation (`/docs`).
- **`POST /legal_assistant`**: Accepts a `LegalQueryRequest`, executes guardrails and the ReAct agent, and returns:
  ```json
  {
      "status": "success",
      "query": "...",
      "response": "...",
      "retrived context": [...],
      "timestamp": "..."
  }
  ```

### Frontend (`Legal_graph/frontend/`)
- **`index.html`**: Professional single-page application styled with Tailwind CSS (light/dark theme support, sidebar with suggested legal inquiries & recent history, interactive settings modal).
- **`script.js`**: Dynamic state management, robust `marked.js` markdown rendering (safely handling strings, arrays, and objects), API health checking, clipboard copying, and **collapsible retrieved legal context source drawers**.
- **`style.css`**: Glassmorphic panels, custom scrollbars, and typography optimized with *Plus Jakarta Sans* and *JetBrains Mono*.

---

## 🚀 Quickstart & Installation

### 1. Clone & Setup Environment
```bash
git clone https://github.com/Manan79/Legal_AI_Assistant_V2.git
cd Legal_AI_Assitant_V2
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
OPENROUTER_API_KEY=your_openrouter_key
AZURE_OPENAI_KEY=your_azure_key
FOUNDRY_API_KEY=your_foundry_key
TAVILY_API_KEY=your_tavily_key
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT_NAME=Legal_AI_Evals_V2
FAST_MODEL=openai/gpt-4o-mini
```

### 3. Start Qdrant Vector Database
Ensure Qdrant is running locally on port 6333:
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 4. Run the FastAPI Application
```bash
python Legal_graph/Backend/main.py
```
Open your browser at **`http://localhost:8000/`** to access the web UI, or explore Swagger docs at **`http://localhost:8000/docs`**.

---

## 🧪 Running Tests & Evaluations

- **Test Hybrid Retriever**:
  ```bash
  python Legal_graph/testing/test_retriever_suite.py
  ```
- **Test Guardrails**:
  ```bash
  python Legal_graph/testing/test_guardrails_script.py
  ```
- **Run LangSmith Evaluations**:
  ```bash
  python Legal_graph/testing/Eval_testing.py
  ```

---

## 👥 Authors & Attribution

Developed with precision for advanced legal AI applications.
