import operator
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    query: str
    doc_source: str | None  # optional url filter for semantic search
    context: str
    plan: str
    code: str
    error: str
    messages: Annotated[Sequence[BaseMessage], operator.add]
