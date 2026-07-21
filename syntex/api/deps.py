from syntex.agents.graph import create_agent_graph
from syntex.ingestion.vector_store import VectorStore
from syntex.core.logger import logger

# globally cache instances
_graph_instance = None
_vector_store_instance = None

def get_graph():
    # lazy load and return the compiled langgraph instance
    global _graph_instance
    if _graph_instance is None:
        logger.info("compiling agent graph for api use")
        _graph_instance = create_agent_graph()
    return _graph_instance

def get_vector_store():
    # lazy load the vector store instance
    global _vector_store_instance
    if _vector_store_instance is None:
        logger.info("initializing vector store for api routes")
        _vector_store_instance = VectorStore()
    return _vector_store_instance
