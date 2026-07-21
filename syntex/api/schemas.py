from pydantic import BaseModel
from typing import Optional

# schema for agent queries
class QueryRequest(BaseModel):
    query: str
    doc_source: str | None = None

# schema for api health check
class HealthResponse(BaseModel):
    status: str
    version: str

# schema for server-sent events (sse) streaming
class AgentEvent(BaseModel):
    agent: str
    status: str
    message: Optional[str] = None
    data: Optional[str] = None

# schema for document ingestion requests
class IngestRequest(BaseModel):
    url: str

# schema for document ingestion responses
class IngestResponse(BaseModel):
    status: str
    url: str
    chunks_processed: int
