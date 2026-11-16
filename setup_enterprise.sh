#!/bin/bash
set -e

echo "=================================================="
echo "  Setting Up Final Enterprise Architecture"
echo "=================================================="

# 1. Create directories
mkdir -p config data exports/reports src/core src/models src/rag src/agents src/tools src/interfaces tests/unit tests/integration .github/workflows

# 2. Create package init files
touch config/__init__.py src/__init__.py src/core/__init__.py src/models/__init__.py src/rag/__init__.py src/agents/__init__.py src/tools/__init__.py src/interfaces/__init__.py tests/__init__.py tests/unit/__init__.py tests/integration/__init__.py

# 3. Create pyproject.toml for package installation and clean imports
cat << 'PKG' > pyproject.toml
[build-system]
requires = ["setuptools>=61.0.0"]
build-backend = "setuptools.build_meta"

[project]
name = "sara-financial-ai"
version = "0.3.0"
description = "Enterprise AI agent for financial reconciliation and auditing"
authors = [{ name = "AI Engineer" }]
dependencies = [
    "langchain>=0.3.0",
    "langchain-core>=0.3.0",
    "langchain-community>=0.3.0",
    "langchain-chroma>=0.1.0",
    "langgraph>=0.2.0",
    "langgraph-checkpoint-sqlite>=2.0.0",
    "chromadb>=0.5.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0"
]
PKG

# 4. Move and organize existing files if they exist in old locations
[ -f src/llm_factory.py ] && mv src/llm_factory.py src/core/llm_factory.py
[ -f src/rag_engine.py ] && mv src/rag_engine.py src/rag/vector_store.py
[ -f src/agent_tools.py ] && mv src/agent_tools.py src/tools/agent_tools.py
[ -f src/agent_workflow.py ] && mv src/agent_workflow.py src/agents/workflow.py

echo "✅ Enterprise folder structure and pyproject.toml created successfully!"
