from syntex.agents.graph import create_agent_graph
from syntex.core.logger import logger

# globally cache the compiled graph
_graph_instance = None

def get_graph():
    # lazy load and return the compiled langgraph instance
    global _graph_instance
    if _graph_instance is None:
        logger.info("compiling agent graph for api use")
        _graph_instance = create_agent_graph()
    return _graph_instance
