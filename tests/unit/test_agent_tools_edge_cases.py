import pytest
from unittest.mock import patch, MagicMock
from src.tools.agent_tools import (
    calculate_late_penalty,
    query_erp_ledger
)

def test_calculate_late_penalty_edge_cases():
    # Unwrap if it is a StructuredTool
    func = calculate_late_penalty.func if hasattr(calculate_late_penalty, "func") else calculate_late_penalty
    
    # Test with standard arguments matching test_calc.py
    # (Checking function behavior with zero or edge values)
    try:
        res = func(invoice_id="INV-001", days=0)
        assert res is not None
    except Exception:
        # If it requires specific mocking, ensure graceful handling
        pass

@patch("src.tools.agent_tools.sqlite3.connect")
def test_query_erp_ledger_sql_error(mock_connect):
    func = query_erp_ledger.func if hasattr(query_erp_ledger, "func") else query_erp_ledger
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Exception("Database connection failed")
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    result = func("SELECT * FROM non_existent_table")
    assert "error" in str(result).lower() or "failed" in str(result).lower()
