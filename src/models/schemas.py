from pydantic import BaseModel, Field
from typing import List, Optional

class InvoiceItem(BaseModel):
    item_no: int = Field(..., description="Line item number")
    description: str = Field(..., description="Description of service or product")
    amount: float = Field(..., description="Line item dollar amount")

class InvoiceRecord(BaseModel):
    invoice_id: str = Field(..., description="Unique invoice identifier, e.g., INV-9942")
    client_name: str = Field(..., description="Name of the client organization")
    vendor_name: str = Field(..., description="Name of the vendor issuing the invoice")
    invoice_date: str = Field(..., description="Date the invoice was issued")
    payment_terms: str = Field(..., description="Payment terms, e.g., Net 30")
    items: List[InvoiceItem] = Field(..., description="List of invoice line items")
    total_amount: float = Field(..., description="Total invoice amount due")

class ERPLedgerRecord(BaseModel):
    client_name: str = Field(..., description="Client name in ERP billing database")
    account_status: str = Field(..., description="Account status, e.g., Active - Net 30")
    outstanding_balance: float = Field(..., description="Current outstanding balance")
    credit_limit: float = Field(..., description="Approved credit limit")
    last_payment_date: str = Field(..., description="Date of last recorded payment")

class AuditReportOutput(BaseModel):
    invoice_id: str
    client_name: str
    rag_total: float
    erp_balance: float
    status_match: bool
    credit_limit_utilized_pct: float
    late_penalty: float
    final_payable: float
    recommendation: str
