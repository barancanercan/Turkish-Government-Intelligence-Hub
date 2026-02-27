"""
Supervisor Agent
Routes queries to appropriate agents
"""

from typing import Literal
import logging

from .state import AgentState, QueryType, Message
from .prompts import get_supervisor_prompt

logger = logging.getLogger(__name__)


def supervisor_node(state: AgentState) -> AgentState:
    """
    Supervisor node - analyzes query and determines next step.

    Args:
        state: Current agent state

    Returns:
        Updated state with routing decision
    """
    query = state.query

    parties = extract_parties(query)
    query_type = classify_query(query)

    state.query_type = QueryType(type=query_type, parties=parties, confidence=0.8)

    if query_type == "comparison":
        state.steps.append("Supervisor: Karşılaştırma sorgusu tespit edildi")
    else:
        state.steps.append("Supervisor: Basit sorgu tespit edildi")

    state.messages.append(Message(role="assistant", content=f"Sorgu türü: {query_type}"))

    return state


def extract_parties(query: str) -> list:
    """Extract mentioned parties from query."""
    known_parties = ["CHP", "AKP", "MHP", "İYİ", "DEM", "SP", "ZP", "BBP"]
    found = []
    query_upper = query.upper()

    for party in known_parties:
        if party in query_upper:
            found.append(party)

    return found


def classify_query(query: str) -> str:
    """Classify query type."""
    query_lower = query.lower()

    if "nasıl kimdir" in query_lower or "kimdir nasıl" in query_lower:
        return "simple"

    comparison_words = ["karşılaştır", "fark", "benzer", "hangisi daha", "vs", "veya", "kıyasla"]
    if any(word in query_lower for word in comparison_words):
        return "comparison"

    research_words = ["araştır", "detaylı", "incele", "nedir", "tarihçe", "biyografi"]
    if any(word in query_lower for word in research_words):
        return "deep_research"

    kişi_words = ["kimdir", "kimdir?", "kimdir nasıl", "kaç yaşında", "nereli", "ne iş yapar"]
    if any(word in query_lower for word in kişi_words):
        return "simple"

    return "simple"


def should_continue_supervisor(state: AgentState) -> Literal["analyst", "researcher"]:
    """
    Determine next step based on query type.

    Args:
        state: Current state

    Returns:
        Next node name
    """
    if state.query_type and state.query_type.type == "comparison":
        return "analyst"
    return "researcher"
