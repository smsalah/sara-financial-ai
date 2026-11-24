from unittest.mock import MagicMock, patch
from src.agents.workflow import run_reconciliation_agent


@patch("src.agents.workflow.SqliteSaver")
@patch("src.agents.workflow.get_llm")
@patch("src.agents.workflow.RAGEngine")
@patch("src.agents.workflow.create_agent")
def test_run_reconciliation_agent(
    mock_create_agent, mock_rag_engine, mock_get_llm, mock_sqlite_saver
):
    """Verify run_reconciliation_agent initializes RAGEngine, LLM, checkpointer, and agent executor."""
    mock_checkpointer = MagicMock()
    mock_sqlite_saver.from_conn_string.return_value.__enter__.return_value = (
        mock_checkpointer
    )

    mock_executor = MagicMock()
    mock_executor.stream.return_value = []
    mock_create_agent.return_value = mock_executor

    run_reconciliation_agent()

    mock_rag_engine.assert_called_once()
    mock_get_llm.assert_called_once()
    mock_sqlite_saver.from_conn_string.assert_called_once()
    mock_create_agent.assert_called_once()
    assert mock_executor.stream.call_count == 2
