import os
from unittest.mock import patch
import pytest
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
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


class DeterministicFakeEmbeddings(Embeddings):
    """Lightweight offline embeddings for CI test runs."""

    def __init__(self, size: int = 8):
        self.size = size

    def _embed(self, text: str) -> list[float]:
        seed = sum(ord(ch) for ch in text) % 997
        return [((seed + i * 17) % 100) / 100.0 for i in range(self.size)]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


class FakeAuditChatModel(BaseChatModel):
    """Deterministic chat model supporting tool calls and multi-turn memory in tests."""

    bound_tools: list = []

    @property
    def _llm_type(self) -> str:
        return "fake-audit-chat-model"

    def bind_tools(self, tools, **kwargs):
        return FakeAuditChatModel(bound_tools=list(tools))

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager=None,
        **kwargs,
    ) -> ChatResult:
        last_msg = messages[-1]

        if isinstance(last_msg, ToolMessage):
            content = (
                "Audit for Zumzum Enterprise Solutions UK (INV-9942): "
                "Outstanding balance is $20,500.00 and credit limit is $50,000.00."
            )
            return ChatResult(
                generations=[ChatGeneration(message=AIMessage(content=content))]
            )

        if (
            isinstance(last_msg, HumanMessage)
            and "credit limit" in last_msg.content.lower()
        ):
            prior_text = " ".join(
                m.content for m in messages if isinstance(m.content, str)
            )
            if "50,000" in prior_text or "50000" in prior_text:
                reply = "Their exact credit limit is $50,000.00."
            else:
                reply = "Credit limit not found in session history."
            return ChatResult(
                generations=[ChatGeneration(message=AIMessage(content=reply))]
            )

        if self.bound_tools:
            tool_call = {
                "name": "query_erp_ledger",
                "args": {"client_name": "Zumzum Enterprise Solutions UK"},
                "id": "call_erp_zumzum_1",
                "type": "tool_call",
            }
            return ChatResult(
                generations=[
                    ChatGeneration(
                        message=AIMessage(content="", tool_calls=[tool_call])
                    )
                ]
            )

        return ChatResult(
            generations=[
                ChatGeneration(
                    message=AIMessage(
                        content="Zumzum Enterprise Solutions UK balance is $20,500.00."
                    )
                )
            ]
        )


@pytest.fixture(scope="function")
def test_db_path(tmp_path):
    # Use a temporary SQLite database for isolated test execution
    db_file = tmp_path / "test_checkpoints.sqlite"
    return str(db_file)


def test_sqlite_checkpointer_persistence(test_db_path, tmp_path):
    # 1. Setup sample document ingestion with isolated Chroma directory and fake embeddings
    sample_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "sample_invoice.txt"
        )
    )
    chroma_dir = str(tmp_path / "chroma_test_db")

    with (
        patch(
            "src.rag.vector_store.get_embeddings",
            return_value=DeterministicFakeEmbeddings(),
        ),
        patch(
            "tests.integration.test_agent_persistence.get_llm",
            return_value=FakeAuditChatModel(),
        ),
    ):
        rag = RAGEngine(persist_directory=chroma_dir)
        if os.path.exists(sample_file):
            rag.ingest_document(sample_file)

        llm = get_llm()
        tools = [
            search_invoice_records,
            calculate_late_penalty,
            query_erp_ledger,
            export_audit_report,
        ]
        system_prompt = (
            "You are an expert Enterprise Financial Audit Agent. "
            "Cross-reference RAG and ERP records."
        )

        thread_config = {"configurable": {"thread_id": "integration_test_session_1"}}

        # 2. Turn 1: Initial Audit Request
        with SqliteSaver.from_conn_string(test_db_path) as checkpointer:
            agent_executor = create_agent(
                model=llm,
                tools=tools,
                system_prompt=system_prompt,
                checkpointer=checkpointer,
            )

            query_1 = (
                "Audit Invoice INV-9942 for Zumzum Enterprise Solutions UK "
                "and check their ERP status."
            )
            events_1 = list(
                agent_executor.stream(
                    {"messages": [HumanMessage(content=query_1)]},
                    config=thread_config,
                    stream_mode="values",
                )
            )

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

            ai_msg_2 = events_2[-1]["messages"][-1]
            assert ai_msg_2.type == "ai"
            assert "50,000" in ai_msg_2.content or "50000" in ai_msg_2.content
