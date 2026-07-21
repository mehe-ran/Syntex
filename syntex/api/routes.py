import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from syntex.api.schemas import HealthResponse, QueryRequest, IngestRequest, IngestResponse
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

@router.post("/ingest", response_model=IngestResponse)
async def ingest_documentation(request: IngestRequest, vector_store=Depends(get_vector_store)):
    # process and store a new documentation url dynamically
    scraper = DocScraper()
    chunker = DocChunker()
    
    # scrape the html
    raw_text = scraper.scrape_url(request.url)
    if not raw_text:
        raise HTTPException(status_code=400, detail="failed to scrape the provided url")
        
    # split into semantic chunks
    chunks = chunker.chunk_text(raw_text)
    if not chunks:
        raise HTTPException(status_code=400, detail="no extractable text found at url")
        
    # store embeddings
    vector_store.add_chunks(chunks, source_url=request.url)
    
    return IngestResponse(
        status="success",
        url=request.url,
        chunks_processed=len(chunks)
    )
