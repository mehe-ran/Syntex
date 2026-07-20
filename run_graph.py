from syntex.agents.graph import create_agent_graph
from syntex.core.logger import logger

def test_graph():
    # compile the multi-agent graph
    graph = create_agent_graph()
    
    # define the initial state with a test query
    initial_state = {
        "query": "how do i define a path parameter in fastapi with a type hint?",
        "context": "",
        "plan": "",
        "code": "",
        "error": "",
        "messages": []
    }
    
    logger.info("--- starting graph execution ---")
    
    # invoke the graph and trace the output
    final_state = graph.invoke(initial_state)
    
    logger.info("--- execution complete ---")
    print("\n[final generated code]\n")
    print(final_state.get("code"))

if __name__ == "__main__":
    test_graph()
