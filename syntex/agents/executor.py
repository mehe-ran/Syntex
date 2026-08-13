import ast
import re
from langchain_core.messages import AIMessage
from syntex.agents.state import AgentState
from syntex.core.logger import logger

def extract_python_code(markdown_text: str) -> str:
    # try to extract ```python blocks
    python_blocks = re.findall(r'```(?:python)?\s*\n(.*?)```', markdown_text, re.DOTALL)
    if python_blocks:
        return "\n".join(python_blocks)
    return markdown_text # fallback to full text if no blocks found

def executor_node(state: AgentState) -> dict:
    code = state.get("code", "")
    
    logger.info("[executor] validating syntax of generated code")

    clean_code = extract_python_code(code)
    
    try:
        # deterministically check if the code compiles to a valid AST
        ast.parse(clean_code)
        
        # syntax is valid, pass to reviewer
        error_state = ""
        trace_msg = AIMessage(content="syntax validation passed. forwarding to reviewer.", name="Executor")
        
    except SyntaxError as e:
        # catch syntax/indentation errors early and return immediately
        error_state = f"SyntaxError on line {e.lineno}: {e.msg}\nCode snippet:\n{e.text}"
        trace_msg = AIMessage(content=f"syntax validation failed: {error_state}", name="Executor")
        logger.warning(f"[executor] syntax validation failed: {e.msg}")
        
    except Exception as e:
        # catch any other unexpected parsing errors
        error_state = f"Parse Error: {str(e)}"
        trace_msg = AIMessage(content=f"syntax validation failed: {error_state}", name="Executor")
        logger.warning(f"[executor] validation encountered an error: {e}")
        
    return {"error": error_state, "messages": [trace_msg]}
