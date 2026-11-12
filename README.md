# Sara Financial AI 🏦🤖

> An enterprise-grade, privacy-first AI agent designed for automated financial reconciliation, document auditing, and late penalty calculations—running 100% locally with zero cloud API dependencies.

---

## 🏛️ Architectural Overview

**Sara Financial AI** is built on a modular, decoupled architecture that strictly separates **probabilistic reasoning** (orchestrated by advanced local LLMs) from **deterministic computation** (executed via rigorous Python tools and vector similarity search).

```
[ User Prompt ] 
       │
       ▼
[ LangGraph ReAct Agent ] ──(Tool Binding)──► [ search_invoice_records ] ──► [ ChromaDB (Vector Store) ]
       │                                                                               │
       └─────────────────────────► [ calculate_late_penalty ] ◄──────────────────────┘
                                          │
                                          ▼
                            [ Executive Audit Report ]

```

### Core Design Patterns

* **Factory Pattern (`llm_factory.py`)**: Abstracted model instantiation allowing seamless toggling between local open-weights models (Ollama) and cloud providers (OpenAI, Google Gemini).
* **ReAct Agentic Workflow**: Powered by **LangGraph**, enabling the agent to autonomously reason, call vector search tools, execute mathematical Python functions, and synthesize structured compliance reports.
* **Absolute Path State Persistence**: Robust vector persistence via `ChromaDB` ensuring state consistency across ingestion and multi-step tool execution.

---

## 🚀 Tech Stack

* **Core Language**: Python 3.10+
* **Orchestration & Agents**: LangChain, LangGraph (`create_agent`)
* **Vector Database**: ChromaDB (with persistent disk storage)
* **Embeddings**: Ollama (`nomic-embed-text`)
* **Inference Engine**: Ollama running high-performance open-weights models (`qwen3.8:27b`)
* **Validation & Types**: Pydantic for strict tool parameter validation and type coercion

---

## 🗓️ Development Milestones

| Milestone | Status | Description |
| --- | --- | --- |
| **Milestone 1: Local RAG Engine** | ✅ Complete | Air-gapped document ingestion, text chunking, embedding generation, and persistent vector storage using ChromaDB. |
| **Milestone 2: Autonomous ReAct Agent** | ✅ Complete | LangGraph agentic workflow with custom tools for vector search and financial penalty calculations, verified on `qwen3.8:27b`. |
| **Milestone 3: ERP / SQL Database Integration** | 🔄 Planned | Connecting the agent to live SQLite/PostgreSQL billing ledgers for automated cross-referencing against enterprise ERP records. |

---

## 📂 Project Structure

```text
sara-financial-ai/
├── data/
│   └── sample_invoice.txt       # Sample enterprise invoice & payment terms
├── src/
│   ├── __init__.py
│   ├── config.py                # Environment and path configurations
│   ├── llm_factory.py           # LLM and embedding provider abstraction
│   ├── rag_engine.py            # ChromaDB RAG ingestion and query engine
│   ├── agent_tools.py           # Deterministic search and calculation tools
│   └── agent_workflow.py        # LangGraph ReAct agent executor
├── chroma_db/                   # Persistent vector store directory
├── .env                         # Local environment variables
├── requirements.txt             # Project dependencies
└── README.md

```

---

## 🛠️ Getting Started & Installation

### 1. Prerequisites

* Python 3.10 or higher installed.
* [Ollama](https://ollama.com/) installed and running locally.

### 2. Clone and Setup Environment

```bash
git clone https://github.com/your-username/sara-financial-ai.git
cd sara-financial-ai

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

```

### 3. Pull Required Local Models

```bash
ollama pull qwen3.8:27b
ollama pull nomic-embed-text

```

### 4. Configure Environment Variables (`.env`)

Create a `.env` file in the root directory:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen3.8:27b
OLLAMA_EMBED_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434

```

### 5. Run the Autonomous Audit Agent

Execute the Milestone 2 workflow to ingest sample invoices and run a complete multi-step audit:

```bash
python -m src.agent_workflow

```

---

## 📄 License

This project is licensed under the MIT License.