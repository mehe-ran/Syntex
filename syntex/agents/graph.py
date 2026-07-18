from langgraph.graph import StateGraph, START, END
from syntex.agents.state import AgentState
from syntex.agents.researcher import researcher_node
from syntex.agents.planner import planner_node
from syntex.agents.coder import coder_node
from syntex.agents.reviewer import reviewer_node

def route_review(state: AgentState) -> str:
    # route back to coder if errors exist, otherwise finish
    if state.get("error"):
        return "coder"
    return END

def create_agent_graph():
    # initialize the graph with our state schema
    workflow = StateGraph(AgentState)
    
    # register the available agents
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("reviewer", reviewer_node)
    
    # define the standard execution flow
    workflow.add_edge(START, "researcher")
    workflow.add_edge("researcher", "planner")
    workflow.add_edge("planner", "coder")
    workflow.add_edge("coder", "reviewer")
    
    # define conditional routing logic based on the reviewer's output
    workflow.add_conditional_edges("reviewer", route_review)
    
    # compile into an executable application
    return workflow.compile()
