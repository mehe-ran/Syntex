import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from syntex.api.schemas import HealthResponse, QueryRequest
from syntex.api.deps import get_graph

# initialize the api router
router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    # verify the api is responsive
    return HealthResponse(status="ok", version="0.1.0")

@router.post("/query/stream")
async def stream_query(request: QueryRequest, graph=Depends(get_graph)):
    # stream the agent graph execution via server-sent events
    async def event_generator():
        initial_state = {"query": request.query}
        
        # iterate through the graph events as they happen
        for output in graph.stream(initial_state):
            for node_name, state_update in output.items():
                event_data = {
                    "agent": node_name,
                    "status": "processing",
                    "data": state_update.get("code", "") if node_name == "coder" else ""
                }
                # yield formatted sse chunk
                yield f"data: {json.dumps(event_data)}\n\n"
                
    return StreamingResponse(event_generator(), media_type="text/event-stream")
