# 🏛️ Sara Financial AI: System Architecture & Design Specification

## 1. Executive Summary

**Sara Financial AI** is an enterprise-grade autonomous financial auditing and RAG (Retrieval-Augmented Generation) reconciliation agent. Designed for strict financial compliance, it bridges unstructured invoice documents with structured SQL ledger transactions, computes automated late-penalties, maintains persistent multi-turn conversational memory, and exposes its capabilities via a dual-interface stack (FastAPI REST backend and Streamlit visual frontend).

---

## 2. High-Level System Architecture

The application is containerized via **Docker Compose**, orchestrating two primary runtime services backed by persistent SQLite checkpointers and Chroma vector indices.

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

---

## 3. LangGraph Stateful Multi-Turn Workflow

Sara leverages **LangGraph** to manage conversational state, agentic decision loops, and tool orchestration. 

### State Schema (`AgentState`)
The agent maintains state across turns using a typed dictionary schema:
* `messages`: A history of `BaseMessage` objects representing user prompts, agent thoughts, and tool outputs.
* `audit_context`: A structured dictionary containing active invoice metadata, ledger verification results, and penalty computations.

### Persistence Layer (`SqliteSaver`)
Conversational states are checkpointed to a local SQLite database (`checkpoints.sqlite`). 
* **Thread Isolation**: Each user session or audit thread is identified by a unique `thread_id`.
* **Fault Tolerance**: If the API restarts or containers reboot, active conversation threads can be resumed seamlessly from the SQLite checkpointer without loss of audit context.

---

## 4. RAG Vector Pipeline & Document Ingestion

The RAG engine ensures that unstructured invoice PDFs, receipts, and compliance guidelines are indexed and retrievable during audits.

* **Embedding Model**: Utilizes **Ollama** embeddings (`nomic-embed-text`) running locally to generate dense vector representations.
* **Vector Store**: **ChromaDB** stores and indexes document embeddings for high-performance semantic search.
* **Retrieval Workflow**:
  1. Incoming audit queries trigger semantic searches across stored invoice vectors.
  2. Top-k relevant chunks are retrieved and injected into the LLM context window.
  3. The agent cross-references the retrieved text chunks against structured SQL ledger records.

---

## 5. Enterprise Tools & Database Layer

The agent is equipped with deterministic execution tools to guarantee mathematical and transactional accuracy:
* **ERP SQL Ledger (`data/erp_ledger.db`)**: A relational database containing official invoice records, client credit limits, and payment statuses.
* **Late Penalty Engine**: Automatically calculates accrued late fees based on invoice due dates and enterprise grace-period rules.
* **Report Exporter**: Generates structured audit reports and exports them as CSV/PDF artifacts into the `./exports/` volume.

---

## 6. Security & Containerization

* **Container Runtime**: Built on `python:3.10-slim` with explicitly compiled `libsqlite3-dev` and build essentials to ensure reliable native C-extension execution.
* **Environment Configuration**: Isolated via Docker networks with configurable environment variables (`OLLAMA_BASE_URL`, `API_URL`).