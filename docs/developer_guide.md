# 🛠️ Sara Financial AI — Developer & Contributor Guide

Welcome to the development guide for **Sara Financial AI**. This document provides a comprehensive overview of the local development workflow, repository architecture, tool creation guidelines, state extension patterns, and testing practices.

---

## 🏗️ 1. Architecture Overview

Sara Financial AI is built using a modular micro-architecture designed for enterprise financial compliance:
* **`src/agents/`**: Contains LangGraph state definitions, graph compilation, and multi-turn execution nodes.
* **`src/core/`**: Core configuration bindings, environment variables, and LLM factory setups.
* **`src/interfaces/`**: Interface layers including the FastAPI backend (`api.py`) and Streamlit frontend (`frontend.py`).
* **`src/models/`**: Pydantic v2 validation schemas for API requests, tool inputs, and audit responses.
* **`src/rag/`**: ChromaDB vector store management, embedding pipelines via Ollama (`nomic-embed-text`), and invoice ingestion.
* **`src/tools/`**: Deterministic enterprise tools including ERP SQL ledger querying and late-penalty calculations.

---

## 💻 2. Local Environment Setup

To set up your local development environment without Docker:

1. **Clone the repository and create a virtual environment:**
   ```bash
   git clone [https://github.com/smsalah/sara-financial-ai.git](https://github.com/smsalah/sara-financial-ai.git)
   cd sara-financial-ai
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install package dependencies in editable mode:**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Configure environment variables:**
   Ensure your `.env` file matches your local setup (`LLM_PROVIDER=ollama`, `OLLAMA_MODEL=qwen3.8:27b`, `OLLAMA_EMBED_MODEL=nomic-embed-text`, `OLLAMA_BASE_URL=http://localhost:11434`).

---

## 🔧 3. Adding New Enterprise Tools

To add a new auditing or calculation tool to Sara:
1. Create the tool function in `src/tools/` using `@tool`.
2. Register the tool in your LangGraph agent execution node (`src/agents/graph.py`).
3. Write unit tests in `tests/unit/` to verify deterministic outputs under edge cases.

---

## 🤖 4. Extending LangGraph States & Nodes

When adding new multi-turn conversational capabilities or audit states:
1. Update the state schema in `src/agents/state.py`.
2. Implement your node logic in `src/agents/nodes.py` and bind them to the compiled state graph.

---

## 🧪 5. Running the Test Suite

Sara Financial AI uses `pytest` for unit and integration testing.
* **Run all tests with verbose output:**
  ```bash
  pytest tests/ -v
  ```
