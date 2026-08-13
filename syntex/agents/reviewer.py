from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from syntex.agents.state import AgentState
from syntex.core.config import settings
from syntex.core.logger import logger
from syntex.utils.prompts import REVIEWER_SYSTEM_PROMPT

def reviewer_node(state: AgentState) -> dict:
    context = state.get("context", "")
    code = state.get("code", "")
    
    logger.info("[reviewer] validating generated code against documentation")

    # initialize llm inside node with explicitly configured api key
    llm = ChatOpenAI(
        model=settings.model_name,
        temperature=0.0,
        api_key=settings.openai_api_key
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", REVIEWER_SYSTEM_PROMPT),
        ("human", "code:\n{code}\n\ndocs:\n{context}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"code": code, "context": context})
    
    feedback = response.content.strip().lower()
    
    if feedback == "pass":
        error_state = ""
        trace_msg = AIMessage(content="code review passed.", name="Reviewer")
    else:
        error_state = response.content
        trace_msg = AIMessage(content=f"code review failed: {error_state}", name="Reviewer")
    
    return {"error": error_state, "messages": [trace_msg]}
