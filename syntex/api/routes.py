from fastapi import APIRouter
from syntex.api.schemas import HealthResponse, QueryRequest

# initialize the api router
router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    # verify the api is responsive
    return HealthResponse(status="ok", version="0.1.0")

@router.post("/query")
async def process_query(request: QueryRequest):
    # placeholder for the multi-agent workflow
    return {"message": "query received, agent orchestration pending", "query": request.query}
