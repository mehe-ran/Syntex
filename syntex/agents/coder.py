from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from syntex.agents.state import AgentState
from syntex.core.config import settings
from syntex.core.logger import logger

# initialize the llm
llm = ChatOpenAI(model=settings.model_name, temperature=0.1)

def coder_node(state: AgentState) -> dict:
    query = state.get("query", "")
    context = state.get("context", "")
    plan = state.get("plan", "")
    error_feedback = state.get("error", "")
    
    logger.info("[coder] generating code boilerplate")

    # define the system prompt, including error context if the reviewer rejected a previous attempt
    system_instructions = (
        "you are a senior backend engineer. write clean, production-ready code based on the provided plan and api documentation.\n"
        "strictly adhere to the documentation syntax. do not hallucinate endpoints."
    )
    
    if error_feedback:
        system_instructions += f"\nfix the following errors from the previous attempt:\n{error_feedback}"

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instructions),
        ("human", "query: {query}\n\nplan:\n{plan}\n\ndocs:\n{context}")
    ])
    
    # execute the chain
    chain = prompt | llm
    response = chain.invoke({"query": query, "plan": plan, "context": context})
    
    # generate a trace message
    trace_msg = AIMessage(
        content="generated code boilerplate.",
        name="Coder"
    )
    
    return {
        "code": response.content,
        "messages": [trace_msg]
    }
