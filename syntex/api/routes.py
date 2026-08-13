import json
import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from syntex.api.schemas import HealthResponse, QueryRequest, IngestRequest, IngestResponse, QueryResponse
from syntex.api.deps import get_graph, get_vector_store
from syntex.ingestion.scraper import DocScraper
from syntex.ingestion.chunker import DocChunker

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
        
        # add recursion_limit and thread_id memory
        thread_id = request.thread_id or str(uuid.uuid4())
        config = {"recursion_limit": 5, "configurable": {"thread_id": thread_id}}
        for output in graph.stream(initial_state, config):
            for node_name, state_update in output.items():
                event_data = {
                    "agent": node_name,
                    "status": "processing",
                    "data": state_update.get("code", "") if node_name == "coder" else ""
                }
                # yield formatted sse chunk
                yield f"data: {json.dumps(event_data)}\n\n"
                
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/ingest", response_model=IngestResponse)
async def ingest_documentation(request: IngestRequest, vector_store=Depends(get_vector_store)):
    # process and store a new documentation url dynamically
    scraper = DocScraper()
    chunker = DocChunker()
    
    raw_text = scraper.scrape_url(request.url)
    if not raw_text:
        raise HTTPException(status_code=400, detail="failed to scrape the provided url")
        
    chunks = chunker.chunk_text(raw_text)
    if not chunks:
        raise HTTPException(status_code=400, detail="no extractable text found at url")
        
    vector_store.add_chunks(chunks, source_url=request.url)
    
    return IngestResponse(
        status="success",
        url=request.url,
        chunks_processed=len(chunks)
    )

@router.post("/query", response_model=QueryResponse)
async def standard_query(request: QueryRequest, graph=Depends(get_graph)):
    # execute the agent graph synchronously and return the final state
    initial_state = {
        "query": request.query,
        "doc_source": request.doc_source
    }
    
    # add recursion_limit and thread_id memory
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"recursion_limit": 5, "configurable": {"thread_id": thread_id}}
    final_state = graph.invoke(initial_state, config)
    
    return QueryResponse(
        query=request.query,
        code=final_state.get("code", ""),
        error=final_state.get("error")
    )
