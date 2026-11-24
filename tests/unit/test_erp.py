from src.tools.agent_tools import query_erp_ledger


def test_query_erp_ledger_existing_client():
    result = query_erp_ledger.invoke({"client_name": "Zumzum Enterprise Solutions UK"})
    assert "ERP Ledger Record Found" in result
    assert "Zumzum Enterprise Solutions UK" in result
    assert "$20,500.00" in result
    assert "$50,000.00" in result


def test_query_erp_ledger_missing_client():
    result = query_erp_ledger.invoke({"client_name": "Nonexistent Corporation XYZ"})
    assert "No ERP billing ledger records found" in result
