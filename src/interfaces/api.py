import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from src.core.llm_factory import get_llm
from src.tools.agent_tools import search_invoice_records, calculate_late_penalty, query_erp_ledger, export_audit_report
from src.rag.vector_store import RAGEngine

app = FastAPI(
    title="Sara Financial AI - Enterprise API",
    description="Production-grade autonomous financial auditing and reconciliation agent.",
    version="0.3.0"
)

class AuditRequest(BaseModel):
    query: str = Field(..., description="Natural language audit request", example="Audit Invoice INV-9942 for Zumzum Enterprise Solutions UK")
    thread_id: str = Field(default="default_audit_thread", description="Thread ID for persistent multi-turn memory checkpointer")

class AuditResponse(BaseModel):
    thread_id: str
    response: str

@app.on_event("startup")
def startup_event():
    sample_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_invoice.txt"))
    rag = RAGEngine()
    if os.path.exists(sample_file):
        rag.ingest_document(sample_file)

@app.post("/audit", response_model=AuditResponse)
def run_audit(request: AuditRequest):
    try:
        llm = get_llm()
        tools = [search_invoice_records, calculate_late_penalty, query_erp_ledger, export_audit_report]
        system_prompt = (
            "You are an expert Enterprise Financial Audit & Reconciliation Agent. "
            "Cross-reference RAG vector store invoice records and SQLite ERP ledger databases before compiling audit reports."
        )

        db_checkpoint_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "checkpoints.sqlite"))
        
        with SqliteSaver.from_conn_string(db_checkpoint_path) as checkpointer:
            agent_executor = create_agent(model=llm, tools=tools, system_prompt=system_prompt, checkpointer=checkpointer)
            thread_config = {"configurable": {"thread_id": request.thread_id}}

            events = list(agent_executor.stream(
                {"messages": [HumanMessage(content=request.query)]}, 
                config=thread_config, 
                stream_mode="values"
            ))

            final_message = events[-1]["messages"][-1]
            return AuditResponse(
                thread_id=request.thread_id,
                response=final_message.content if final_message.content else "Agent completed tool execution."
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Sara Financial AI API"}
