from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from syntex.agents.state import AgentState
from syntex.core.config import settings
from syntex.core.logger import logger

# initialize the llm
llm = ChatOpenAI(model=settings.model_name, temperature=0.2)

def planner_node(state: AgentState) -> dict:
    query = state.get("query", "")
    context = state.get("context", "")
    
    logger.info("[planner] drafting integration plan based on retrieved context")

    # define the system prompt for the planner
    prompt = ChatPromptTemplate.from_messages([
        ("system", "you are an expert software architect. using the provided api documentation, create a clear, step-by-step integration plan to solve the user's query. do not write code, just the structural steps."),
        ("human", "query: {query}\n\ndocumentation:\n{context}")
    ])
    
    # execute the chain
    chain = prompt | llm
    response = chain.invoke({"query": query, "context": context})
    
    # generate a trace message for the ui
    trace_msg = AIMessage(
        content="drafted the integration plan.",
        name="Planner"
    )
    
    return {
        "plan": response.content,
        "messages": [trace_msg]
    }
