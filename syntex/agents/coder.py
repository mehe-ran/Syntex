from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from syntex.agents.state import AgentState
from syntex.core.config import settings
from syntex.core.logger import logger
from syntex.utils.prompts import CODER_SYSTEM_PROMPT

def coder_node(state: AgentState) -> dict:
    query = state.get("query", "")
    context = state.get("context", "")
    plan = state.get("plan", "")
    error_feedback = state.get("error", "")
    
    logger.info("[coder] generating code boilerplate")

    # initialize llm inside node with explicitly configured api key
    llm = ChatOpenAI(
        model=settings.model_name,
        temperature=0.1,
        api_key=settings.openai_api_key
    )

    system_instructions = CODER_SYSTEM_PROMPT
    if error_feedback:
        system_instructions += f"\nfix the following errors from the previous attempt:\n{error_feedback}"

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instructions),
        ("human", "query: {query}\n\nplan:\n{plan}\n\ndocs:\n{context}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"query": query, "plan": plan, "context": context})
    
    trace_msg = AIMessage(content="generated code boilerplate.", name="Coder")
    
    return {"code": response.content, "messages": [trace_msg]}
