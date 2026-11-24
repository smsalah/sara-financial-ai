from src.tools.agent_tools import calculate_late_penalty


def test_calculate_late_penalty_default():
    result = calculate_late_penalty.invoke({})
    assert "$20,500.00" in result
    assert "$22,037.50" in result
    assert "3" in result


def test_calculate_late_penalty_custom_values():
    result = calculate_late_penalty.invoke(
        {"invoice_total": 10000.00, "months_overdue": 2, "penalty_rate_pct": 3.0}
    )
    # Penalty: 10000 * 0.03 * 2 = 600. Total: 10600.
    assert "$10,000.00" in result
    assert "$600.00" in result
    assert "$10,600.00" in result


def test_calculate_late_penalty_string_parsing():
    result = calculate_late_penalty.invoke(
        {"invoice_total": "$15,000.00", "months_overdue": "4", "penalty_rate_pct": "2%"}
    )
    # Penalty: 15000 * 0.02 * 4 = 1200. Total: 16200.
    assert "$15,000.00" in result
    assert "$1,200.00" in result
    assert "$16,200.00" in result
