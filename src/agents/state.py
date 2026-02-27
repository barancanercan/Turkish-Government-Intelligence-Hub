"""
Agent State Definitions
Pydantic models for LangGraph state management
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Chat message."""

    role: str
    content: str
    name: Optional[str] = None


class DocumentInfo(BaseModel):
    """Document metadata."""

    id: str
    content: str
    source: str
    party: Optional[str] = None
    score: float = 0.0


class QueryType(BaseModel):
    """Query classification."""

    type: str
    parties: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    confidence: float = 0.0

    model_config = {"use_enum_values": True}


class AgentState(BaseModel):
    """
    Main state for LangGraph agent workflow.
    Passed between all agents in the pipeline.
    """

    messages: List[Message] = Field(default_factory=list)

    query: str = ""
    query_type: Optional[QueryType] = None

    retrieved_docs: List[DocumentInfo] = Field(default_factory=list)
    web_results: List[Dict[str, str]] = Field(default_factory=list)
    wikipedia_results: List[Dict[str, str]] = Field(default_factory=list)

    analysis: str = ""
    comparison: str = ""

    draft_answer: str = ""
    final_answer: str = ""

    sources: List[str] = Field(default_factory=list)
    citations: List[str] = Field(default_factory=list)

    quality_score: float = 0.0
    feedback: str = ""
    needs_revision: bool = False

    error: Optional[str] = None
    steps: List[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


class MessageState(BaseModel):
    """
    Simple state for chat-like interactions.
    """

    messages: List[Message] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


def create_initial_state(query: str) -> AgentState:
    """
    Create initial state for a new query.

    Args:
        query: User question

    Returns:
        AgentState: Initial state
    """
    return AgentState(
        query=query,
        messages=[Message(role="user", content=query)],
    )


def add_message(state: AgentState, role: str, content: str, name: Optional[str] = None) -> AgentState:
    """
    Add a message to the state.

    Args:
        state: Current state
        role: Message role (user/assistant/system/tool)
        content: Message content
        name: Optional name for tool messages

    Returns:
        Updated state
    """
    new_message = Message(role=role, content=content, name=name)
    state.messages.append(new_message)
    state.steps.append(f"{role}: {content[:50]}...")
    return state
