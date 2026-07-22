from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from syntex.agents.state import AgentState
from syntex.core.config import settings
from syntex.core.logger import logger
from syntex.utils.prompts import PLANNER_SYSTEM_PROMPT

# initialize the llm
llm = ChatOpenAI(model=settings.model_name, temperature=0.2)

def planner_node(state: AgentState) -> dict:
    query = state.get("query", "")
    context = state.get("context", "")
    
    logger.info("[planner] drafting integration plan based on retrieved context")

    # use centralized system prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", PLANNER_SYSTEM_PROMPT),
        ("human", "query: {query}\n\ndocumentation:\n{context}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"query": query, "context": context})
    
    trace_msg = AIMessage(content="drafted the integration plan.", name="Planner")
    
    return {"plan": response.content, "messages": [trace_msg]}
