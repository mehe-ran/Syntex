from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from syntex.agents.state import AgentState
from syntex.core.config import settings
from syntex.core.logger import logger

# initialize the llm with a highly strict configuration
llm = ChatOpenAI(model=settings.model_name, temperature=0.0)

def reviewer_node(state: AgentState) -> dict:
    context = state.get("context", "")
    code = state.get("code", "")
    
    logger.info("[reviewer] validating generated code against documentation")

    # define the system prompt for the reviewer
    prompt = ChatPromptTemplate.from_messages([
        ("system", "you are a strict code reviewer. verify that the provided code only uses endpoints, methods, and parameters explicitly defined in the documentation context.\n"
                   "if it is completely correct, reply only with 'pass'.\n"
                   "if there are errors or hallucinations, explain exactly what is wrong so the coder can fix it."),
        ("human", "code:\n{code}\n\ndocs:\n{context}")
    ])
    
    # execute the chain
    chain = prompt | llm
    response = chain.invoke({"code": code, "context": context})
    
    feedback = response.content.strip().lower()
    
    # determine if the code passed the guardrail
    if feedback == "pass":
        error_state = ""
        trace_msg = AIMessage(content="code review passed.", name="Reviewer")
    else:
        error_state = response.content
        trace_msg = AIMessage(content=f"code review failed: {error_state}", name="Reviewer")
    
    return {
        "error": error_state,
        "messages": [trace_msg]
    }
