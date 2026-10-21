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
│   (Semantic Safety Classification ── PII Detection ── Jailbreak Defenses)│
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

#### LangSmith Experiment Comparison Dashboard
![Experiment Results](docs/assets/experiment%20results.png)
*Comparison across multiple evaluation runs tracking feedback scores (accuracy, faithfulness, legal correctness, retrieval relevance), latency, token consumption, and cost.*

#### LangSmith Traces & Monitoring
![Traces](docs/assets/traces.png)
*Detailed trace monitoring showing model calls distribution, tool invocation breakdown (`get_retrieved_results`, `tavily_search`, `websearch`), error rates, and total cost tracking.*

---

## 🧠 1. Agent Architecture & ReAct Workflow

The core agent (`Legal_graph/Agent/react_agent.py`) is built using **LangGraph** and implements a multi-turn **ReAct (Reasoning + Acting)** execution graph:
1. **Guardrails Interception**: Incoming queries are screened by NeMo Guardrails before agent execution.
2. **Conversation Threading (`thread_id`)**: Utilizes LangGraph's `InMemorySaver` checkpointer with dynamic UUID generation on frontend inquiry resets, isolating multi-turn chat history per session.
3. **Reasoning Step**: The model analyzes the legal question and decides whether to invoke retrieval tools or web search.
4. **Tool Execution**: Calls `get_retrieved_results` (vector search) or `websearch`.
5. **Observation & Synthesis**: Synthesizes retrieved judgments, statutes, and provisions into a structured legal brief.

---

## 🛡️ 2. NeMo Guardrails & Semantic Safety

Implemented via **NeMo Guardrails** (`Legal_graph/Gaurdrails/gaurdrails.py` and `colang_rules.py`):
- **Semantic Safety Classification (`classify_input_safety`)**: Uses an LLM security classifier to inspect user intent, categorizing inputs into `SAFE`, `BLOCK_JAILBREAK`, `BLOCK_OFF_TOPIC`, or `GREETING`. This prevents paraphrased bypasses (e.g. *"brew me a coffee"*, *"disregard prior constraints"*).
- **PII Detection (`detect_pii`)**: Automatically scans input messages for emails, phone numbers, SSNs, API keys, and credit cards using regex patterns.
- **Off-Topic & Jailbreak Defenses**: Strictly blocks non-legal queries and prompt injection attempts (such as DAN mode or system prompt overrides).

---

## 🐳 3. Docker & Production Deployment Strategy

The project is containerized for production readiness using Docker and Docker Compose:
- **`Dockerfile`**: Packages the Python 3.11 runtime, system dependencies, and installs `requirements.txt` layers efficiently.
- **`docker-compose.yml`**: Orchestrates the FastAPI backend container while linking dynamically to your running Qdrant vector database via `host.docker.internal:6333`.
- **Docker Hub Publishing**: You can push pre-built images (`docker push <username>/legal-ai-backend:latest`) to deploy seamlessly across cloud servers without compiling code on production hosts.

---

## 🖥️ 4. Modern Web UI & Interactive Experience

The platform provides a responsive, professional single-page web application served directly by FastAPI (`http://localhost:8000/`):
- **Welcome & Hero State**: Clean, modern light-mode interface featuring quick-start preset legal inquiries (Bail conditions under CrPC, Cyber crime rulings, Commercial contract remedies, Doctrine of judicial review), live API connection status indicators, and dark/light theme toggling.
- **Structured Legal Intelligence**: Generates legally precise Markdown briefs with structured headings, numbered lists, and statutory citations.
- **Expandable Retrieved Legal Context Drawer**: Users can inspect the exact underlying Supreme Court precedent chunks retrieved via Qdrant MMR hybrid search (`Source Precedent Chunk #1`, `Vector MMR`, case citations, and textual evidence).

### 📸 Frontend Demo Screenshots

#### 1. Landing Page & Welcome Dashboard
![Frontend UI](docs/assets/frontend.png)
*The modern light-mode web interface featuring preset legal inquiry cards, active FastAPI connection status, and sidebar navigation.*

#### 2. Structured Legal ReAct Answer
![Legal Response](docs/assets/response.png)
*Formatted markdown answer breaking down complex statutory interpretation and legal provisions with clear headings and numbered lists.*

#### 3. Expandable Retrieved Legal Context & Sources Drawer
![Retrieved Context](docs/assets/context.png)
*Interactive drawer exposing exact precedent chunks and vector MMR source excerpts retrieved from Qdrant.*

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

### 3. Run with Docker Compose
```bash
docker compose up --build -d --remove-orphans
```
Access your web app at **`http://localhost:8000/`**.

---

## 👥 Authors & Attribution

 Developed by Manan Sood.

Co-Authored-By: Claude Code <noreply@anthropic.com>

