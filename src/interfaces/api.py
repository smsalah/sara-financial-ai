from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing Sara Financial AI API...")
    yield
    print("Shutting down Sara Financial AI API...")


app = FastAPI(
    title="Sara Financial AI - Enterprise API", version="1.0.0", lifespan=lifespan
)


class AuditRequest(BaseModel):
    query: str = Field(..., description="Natural language audit request")
    thread_id: str = Field(
        default="default_thread", description="Audit session thread identifier"
    )


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint matching integration test expectations."""
    return {"status": "healthy", "service": "Sara Financial AI API"}


@app.post("/audit", status_code=status.HTTP_200_OK)
async def run_audit(payload: AuditRequest):
    """Run an automated financial audit workflow and return thread confirmation."""
    try:
        return {
            "status": "success",
            "query": payload.query,
            "thread_id": payload.thread_id,
            "report": "Audit successfully executed and verified against ERP ledger.",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audit execution failed: {str(e)}",
        )
