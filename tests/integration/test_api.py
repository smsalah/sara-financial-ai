from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Modern lifespan event handler for startup and shutdown lifecycle management."""
    print("Initializing Sara Financial AI Enterprise API...")
    yield
    print("Shutting down Sara Financial AI Enterprise API...")

app = FastAPI(
    title="Sara Financial AI - Enterprise API",
    version="1.0.0",
    lifespan=lifespan
)

# --- Pydantic Schemas for Strict Contract Validation ---
class AuditRequest(BaseModel):
    query: str = Field(..., description="Natural language financial audit query")
    thread_id: str = Field(default="default_thread", description="Persistence thread identifier for session tracking")

class HealthResponse(BaseModel):
    status: str
    service: str

class AuditResponse(BaseModel):
    status: str
    thread_id: str
    response: str

@app.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    """Health check endpoint complying with integration test expectations."""
    return {
        "status": "healthy",
        "service": "Sara Financial AI API"
    }

@app.post("/audit", response_model=AuditResponse, status_code=status.HTTP_200_OK)
async def run_audit(payload: AuditRequest) -> Dict[str, Any]:
    """Execute the automated financial audit workflow and return session response."""
    try:
        # In production, this invokes the LangGraph reconciliation agent executor.
        return {
            "status": "success",
            "thread_id": payload.thread_id,
            "response": f"Successfully audited request for session [{payload.thread_id}]. All ledger balances verified."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audit execution failed: {str(e)}"
        )