from pydantic import BaseModel, Field


class AuditQuery(BaseModel):
    query: str = Field(..., description="Natural language audit query")
    thread_id: str = Field(default="default_thread", description="Session thread ID")
