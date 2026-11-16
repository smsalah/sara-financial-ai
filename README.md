```python
comprehensive_readme = """# 💼 Sara Financial AI

> **Enterprise-Grade Autonomous Financial Auditing & RAG Reconciliation Agent**

Sara Financial AI is an advanced, production-ready AI agent designed to automate financial auditing workflows. By combining Retrieval-Augmented Generation (RAG) for invoice verification with direct ERP SQL ledger integration, late-penalty calculations, and persistent multi-turn conversational memory, Sara provides accurate, verifiable, and stateful financial audits.

---

## 🌟 Key Features

* **Autonomous Financial Auditing**: Cross-references unstructured invoice documents with structured SQL ledger data.
* **Stateful Multi-Turn Conversations**: Powered by **LangGraph** with persistent SQLite checkpointers (`langgraph-checkpoint-sqlite`) to maintain conversation history across sessions.
* **Dual Interface Stack**: 
  * **FastAPI Backend**: High-performance REST API with automatic Swagger documentation.
  * **Streamlit Frontend**: An intuitive, interactive visual chat interface for auditors and stakeholders.
* **RAG & Vector Search**: Uses **ChromaDB** and Ollama embeddings (`nomic-embed-text`) for lightning-fast invoice and policy retrieval.
* **Enterprise Containerization**: Fully containerized using **Docker Compose** with native SQLite compilation support.

---

## 🏗️ System Architecture


```

```
                           ┌─────────────────────────┐
                           │   Streamlit Chat UI     │ (Port 8501)
                           └────────────┬────────────┘
                                        │ HTTP REST API
                                        ▼
                           ┌─────────────────────────┐
                           │     FastAPI Backend     │ (Port 8000)
                           └────────────┬────────────┘
                                        │
                 ┌──────────────────────┴──────────────────────┐
                 ▼                                             ▼
       ┌───────────────────┐                         ┌───────────────────┐
       │   LangGraph Agent │                         │ Chroma Vector DB  │
       │ (SQLite Checkpoint│                         │ (RAG Ingestion)   │
       └─────────┬─────────┘                         └───────────────────┘
                 │ Tool Execution
                 ▼
       ┌─────────────────────────────────────────────────────────┐
       │ Enterprise Tools: Invoice Search, ERP SQL Ledger,       │
       │ Late Penalty Engine, PDF/CSV Audit Report Exporter      │
       └─────────────────────────────────────────────────────────┘

```

```

---

## 📋 Prerequisites

Before running the application, ensure you have installed:
* **Docker & Docker Compose** (Recommended for containerized deployment)
* **Python 3.10+** (If running locally without Docker)
* **Ollama** running locally with the required models (`qwen3.8:27b` and `nomic-embed-text`)

---

## 🚀 Quick Start (Docker Compose - Recommended)

The entire application stack spins up with a single command using Docker Compose.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/smsalah/sara-financial-ai.git](https://github.com/smsalah/sara-financial-ai.git)
   cd sara-financial-ai

```

2. **Build and start the containers:**
```bash
docker compose up --build -d

```


3. **Access the Application:**
* **Streamlit Visual Chat UI:** [http://localhost:8501](http://localhost:8501)
* **FastAPI Interactive Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Health Check Endpoint:** [http://localhost:8000/health](http://localhost:8000/health)


4. **Stop the containers:**
```bash
docker compose down

```



---

## 💻 Local Development Setup (Without Docker)

If you prefer to run the application directly on your local environment for development:

1. **Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate

```


2. **Install dependencies in editable mode:**
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -e .

```


3. **Start the FastAPI Backend:**
```bash
uvicorn src.interfaces.api:app --host 0.0.0.0 --port 8000 --reload

```


4. **Start the Streamlit Frontend (in a separate terminal):**
```bash
streamlit run src/interfaces/frontend.py --server.port 8501

```



---

## 🔌 API Endpoints & Usage Examples

### 1. Health Check

* **Endpoint:** `GET /health`
* **Example `curl` command:**
```bash
curl -X GET '[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)' -H 'accept: application/json'

```



### 2. Autonomous Financial Audit

* **Endpoint:** `POST /audit`
* **Example `curl` command:**
```bash
curl -X POST '[http://127.0.0.1:8000/audit](http://127.0.0.1:8000/audit)' \\
  -H 'accept: application/json' \\
  -H 'Content-Type: application/json' \\
  -d '{
    "query": "Audit Invoice INV-9942 and check ERP credit limits.",
    "thread_id": "session_001"
  }'

```



---

## 🧪 Running Tests

To run the automated test suite using `pytest`:

```bash
pytest tests/ -v

```

---

## 📁 Project Directory Structure

```text
sara-financial-ai/
├── src/
│   ├── agents/          # LangGraph agent definitions & workflow states
│   ├── core/            # LLM factory and core configuration bindings
│   ├── interfaces/      # FastAPI backend routes & Streamlit UI frontend
│   ├── models/          # Pydantic validation schemas for API & tools
│   ├── rag/             # Chroma vector store management & invoice ingestion
│   └── tools/           # ERP SQL ledger queries & auditing tools
├── tests/               # Unit and integration test suite
├── Dockerfile           # Production container build recipe
├── docker-compose.yml   # Multi-service orchestration configuration
├── pyproject.toml       # Modern Python package metadata & dependencies
└── requirements.txt     # Pinned production dependency versions

```

---

## 📄 License & Professional Standards

Developed under rigorous enterprise engineering standards, featuring modular architecture, robust state management, and containerized deployment workflows.
"""

with open("README.md", "w") as f:
f.write(comprehensive_readme)

print("Comprehensive README.md written successfully.")

```

```text?code_stdout&code_event_index=1
Comprehensive README.md written successfully.


```

I have completely rewritten and expanded the `README.md` file to be exceptionally comprehensive, crystal-clear, and structured for professional evaluation.

### What was improved:

1. **Executive Overview**: Clearly defines what Sara Financial AI is, its core value proposition, and its architectural capabilities.
2. **System Architecture Diagram**: Visualizes how Streamlit, FastAPI, LangGraph, ChromaDB, and enterprise tools interact.
3. **Dual Setup Options**: Step-by-step instructions for both **Docker Compose** (containerized) and **Local Virtual Environment** setups.
4. **API Usage Guide**: Explicit `curl` commands for testing the health check and autonomous audit endpoints.
5. **Detailed Directory Breakdown**: Explains every folder inside `src/` so any developer or auditor instantly understands the codebase layout.

---```python
comprehensive_readme = """# 💼 Sara Financial AI

> **Enterprise-Grade Autonomous Financial Auditing & RAG Reconciliation Agent**

Sara Financial AI is an advanced, production-ready AI agent designed to automate financial auditing workflows. By combining Retrieval-Augmented Generation (RAG) for invoice verification with direct ERP SQL ledger integration, late-penalty calculations, and persistent multi-turn conversational memory, Sara provides accurate, verifiable, and stateful financial audits.

---

## 🌟 Key Features

* **Autonomous Financial Auditing**: Cross-references unstructured invoice documents with structured SQL ledger data.
* **Stateful Multi-Turn Conversations**: Powered by **LangGraph** with persistent SQLite checkpointers (`langgraph-checkpoint-sqlite`) to maintain conversation history across sessions.
* **Dual Interface Stack**: 
  * **FastAPI Backend**: High-performance REST API with automatic Swagger documentation.
  * **Streamlit Frontend**: An intuitive, interactive visual chat interface for auditors and stakeholders.
* **RAG & Vector Search**: Uses **ChromaDB** and Ollama embeddings (`nomic-embed-text`) for lightning-fast invoice and policy retrieval.
* **Enterprise Containerization**: Fully containerized using **Docker Compose** with native SQLite compilation support.

---

## 🏗️ System Architecture


```

```
                           ┌─────────────────────────┐
                           │   Streamlit Chat UI     │ (Port 8501)
                           └────────────┬────────────┘
                                        │ HTTP REST API
                                        ▼
                           ┌─────────────────────────┐
                           │     FastAPI Backend     │ (Port 8000)
                           └────────────┬────────────┘
                                        │
                 ┌──────────────────────┴──────────────────────┐
                 ▼                                             ▼
       ┌───────────────────┐                         ┌───────────────────┐
       │   LangGraph Agent │                         │ Chroma Vector DB  │
       │ (SQLite Checkpoint│                         │ (RAG Ingestion)   │
       └─────────┬─────────┘                         └───────────────────┘
                 │ Tool Execution
                 ▼
       ┌─────────────────────────────────────────────────────────┐
       │ Enterprise Tools: Invoice Search, ERP SQL Ledger,       │
       │ Late Penalty Engine, PDF/CSV Audit Report Exporter      │
       └─────────────────────────────────────────────────────────┘

```

```

---

## 📋 Prerequisites

Before running the application, ensure you have installed:
* **Docker & Docker Compose** (Recommended for containerized deployment)
* **Python 3.10+** (If running locally without Docker)
* **Ollama** running locally with the required models (`qwen3.8:27b` and `nomic-embed-text`)

---

## 🚀 Quick Start (Docker Compose - Recommended)

The entire application stack spins up with a single command using Docker Compose.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/smsalah/sara-financial-ai.git](https://github.com/smsalah/sara-financial-ai.git)
   cd sara-financial-ai

```

2. **Build and start the containers:**
```bash
docker compose up --build -d

```


3. **Access the Application:**
* **Streamlit Visual Chat UI:** [http://localhost:8501](http://localhost:8501)
* **FastAPI Interactive Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Health Check Endpoint:** [http://localhost:8000/health](http://localhost:8000/health)


4. **Stop the containers:**
```bash
docker compose down

```



---

## 💻 Local Development Setup (Without Docker)

If you prefer to run the application directly on your local environment for development:

1. **Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate

```


2. **Install dependencies in editable mode:**
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -e .

```


3. **Start the FastAPI Backend:**
```bash
uvicorn src.interfaces.api:app --host 0.0.0.0 --port 8000 --reload

```


4. **Start the Streamlit Frontend (in a separate terminal):**
```bash
streamlit run src/interfaces/frontend.py --server.port 8501

```



---

## 🔌 API Endpoints & Usage Examples

### 1. Health Check

* **Endpoint:** `GET /health`
* **Example `curl` command:**
```bash
curl -X GET '[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)' -H 'accept: application/json'

```



### 2. Autonomous Financial Audit

* **Endpoint:** `POST /audit`
* **Example `curl` command:**
```bash
curl -X POST '[http://127.0.0.1:8000/audit](http://127.0.0.1:8000/audit)' \\
  -H 'accept: application/json' \\
  -H 'Content-Type: application/json' \\
  -d '{
    "query": "Audit Invoice INV-9942 and check ERP credit limits.",
    "thread_id": "session_001"
  }'

```



---

## 🧪 Running Tests

To run the automated test suite using `pytest`:

```bash
pytest tests/ -v

```

---

## 📁 Project Directory Structure

```text
sara-financial-ai/
├── src/
│   ├── agents/          # LangGraph agent definitions & workflow states
│   ├── core/            # LLM factory and core configuration bindings
│   ├── interfaces/      # FastAPI backend routes & Streamlit UI frontend
│   ├── models/          # Pydantic validation schemas for API & tools
│   ├── rag/             # Chroma vector store management & invoice ingestion
│   └── tools/           # ERP SQL ledger queries & auditing tools
├── tests/               # Unit and integration test suite
├── Dockerfile           # Production container build recipe
├── docker-compose.yml   # Multi-service orchestration configuration
├── pyproject.toml       # Modern Python package metadata & dependencies
└── requirements.txt     # Pinned production dependency versions

```

---

## 📄 License & Professional Standards

Developed under rigorous enterprise engineering standards, featuring modular architecture, robust state management, and containerized deployment workflows.
"""

with open("README.md", "w") as f:
f.write(comprehensive_readme)

print("Comprehensive README.md written successfully.")

```

```text?code_stdout&code_event_index=1
Comprehensive README.md written successfully.


```

I have completely rewritten and expanded the `README.md` file to be exceptionally comprehensive, crystal-clear, and structured for professional evaluation.

### What was improved:

1. **Executive Overview**: Clearly defines what Sara Financial AI is, its core value proposition, and its architectural capabilities.
2. **System Architecture Diagram**: Visualizes how Streamlit, FastAPI, LangGraph, ChromaDB, and enterprise tools interact.
3. **Dual Setup Options**: Step-by-step instructions for both **Docker Compose** (containerized) and **Local Virtual Environment** setups.
4. **API Usage Guide**: Explicit `curl` commands for testing the health check and autonomous audit endpoints.
5. **Detailed Directory Breakdown**: Explains every folder inside `src/` so any developer or auditor instantly understands the codebase layout.

---