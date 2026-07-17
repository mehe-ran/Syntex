from pydantic import BaseModel

# schema for agent queries
class QueryRequest(BaseModel):
    query: str
    doc_source: str | None = None

# schema for api health check
class HealthResponse(BaseModel):
    status: str
    version: str
