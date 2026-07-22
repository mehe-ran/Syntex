from langchain_core.messages import AIMessage
from syntex.agents.state import AgentState
from syntex.ingestion.vector_store import VectorStore
from syntex.core.logger import logger

# initialize a shared vector store instance
vector_store = VectorStore(collection_name="syntex_test")

def researcher_node(state: AgentState) -> dict:
    query = state.get("query", "")
    doc_source = state.get("doc_source")
    
    logger.info(f"[researcher] searching docs for: {query} (filter: {doc_source})")
    
    # execute semantic search with optional metadata filter
    results = vector_store.search(query, n_results=3, source_filter=doc_source)
    
    context_blocks = []
    for res in results:
        source = res["metadata"].get("source", "unknown")
        context_blocks.append(f"--- Source: {source} ---\n{res['content']}")
        
    compiled_context = "\n\n".join(context_blocks) if context_blocks else "No relevant documentation found."
        
    trace_msg = AIMessage(
        content=f"Retrieved {len(results)} chunks of documentation.",
        name="Researcher"
    )
    
    return {"context": compiled_context, "messages": [trace_msg]}
