import os
import pytest
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from src.core.llm_factory import get_llm
from src.tools.agent_tools import (
    search_invoice_records,
    calculate_late_penalty,
    query_erp_ledger,
    export_audit_report,
)
from src.rag.vector_store import RAGEngine


@pytest.fixture(scope="function")
def test_db_path(tmp_path):
    # Use a temporary SQLite database for isolated test execution
    db_file = tmp_path / "test_checkpoints.sqlite"
    return str(db_file)


def test_sqlite_checkpointer_persistence(test_db_path):
    # 1. Setup sample document ingestion
    sample_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "sample_invoice.txt"
        )
    )
    rag = RAGEngine()
    if os.path.exists(sample_file):
        rag.ingest_document(sample_file)

    llm = get_llm()
    tools = [
        search_invoice_records,
        calculate_late_penalty,
        query_erp_ledger,
        export_audit_report,
    ]
    system_prompt = "You are an expert Enterprise Financial Audit Agent. Cross-reference RAG and ERP records."

    thread_config = {"configurable": {"thread_id": "integration_test_session_1"}}

    # 2. Turn 1: Initial Audit Request
    with SqliteSaver.from_conn_string(test_db_path) as checkpointer:
        agent_executor = create_agent(
            model=llm,
            tools=tools,
            system_prompt=system_prompt,
            checkpointer=checkpointer,
        )

        query_1 = "Audit Invoice INV-9942 for Zumzum Enterprise Solutions UK and check their ERP status."
        events_1 = list(
            agent_executor.stream(
                {"messages": [HumanMessage(content=query_1)]},
                config=thread_config,
                stream_mode="values",
            )
        )

        # Verify AI responded in Turn 1
        ai_msg_1 = events_1[-1]["messages"][-1]
        assert ai_msg_1.type == "ai"
        assert "Zumzum" in ai_msg_1.content or "20,500" in ai_msg_1.content

    # 3. Turn 2: Persistent State Follow-up (Reopening checkpoint connection on same thread_id)
    with SqliteSaver.from_conn_string(test_db_path) as checkpointer_reopened:
        agent_executor_reopened = create_agent(
            model=llm,
            tools=tools,
            system_prompt=system_prompt,
            checkpointer=checkpointer_reopened,
        )

        query_2 = "Based on that audit, what is their exact credit limit?"
        events_2 = list(
            agent_executor_reopened.stream(
                {"messages": [HumanMessage(content=query_2)]},
                config=thread_config,
                stream_mode="values",
            )
        )

        # Verify Turn 2 successfully retrieved memory and answered the credit limit question
        ai_msg_2 = events_2[-1]["messages"][-1]
        assert ai_msg_2.type == "ai"
        assert "50,000" in ai_msg_2.content or "50000" in ai_msg_2.content
