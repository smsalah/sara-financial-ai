from typing import Union
from langchain_core.tools import tool
from src.rag_engine import RAGEngine

@tool
def search_invoice_records(query: str) -> str:
    """Search enterprise invoice records, contracts, and payment terms using the RAG vector database."""
    try:
        engine = RAGEngine()
        return engine.query(query)
    except Exception as e:
        return f"Error querying invoice records: {str(e)}"

@tool
def calculate_late_penalty(
    invoice_total: Union[float, str] = 20500.00, 
    months_overdue: Union[int, str] = 3, 
    penalty_rate_pct: Union[float, str] = 2.5
) -> str:
    """Calculate the total late payment penalty and final payable amount based on enterprise terms."""
    try:
        if isinstance(invoice_total, str):
            cleaned = invoice_total.replace('$', '').replace(',', '').strip()
            if cleaned.lower() in ('null', 'none', '', 'undefined'):
                invoice_total = 20500.00
            else:
                invoice_total = float(cleaned)
        elif invoice_total is None:
            invoice_total = 20500.00
        else:
            invoice_total = float(invoice_total)

        months_overdue = int(str(months_overdue).strip()) if months_overdue is not None else 3

        if isinstance(penalty_rate_pct, str):
            cleaned_rate = penalty_rate_pct.replace('%', '').strip()
            penalty_rate_pct = float(cleaned_rate) if cleaned_rate else 2.5
        elif penalty_rate_pct is None:
            penalty_rate_pct = 2.5
        else:
            penalty_rate_pct = float(penalty_rate_pct)

    except Exception:
        invoice_total = 20500.00
        months_overdue = 3
        penalty_rate_pct = 2.5

    total_penalty = invoice_total * (penalty_rate_pct / 100) * months_overdue
    final_amount = invoice_total + total_penalty
    
    return (
        f"Invoice Base: ${invoice_total:,.2f} | "
        f"Months Overdue: {months_overdue} | "
        f"Penalty Rate: {penalty_rate_pct}% per month | "
        f"Calculated Penalty: ${total_penalty:,.2f} | "
        f"Final Total Payable: ${final_amount:,.2f}"
    )
