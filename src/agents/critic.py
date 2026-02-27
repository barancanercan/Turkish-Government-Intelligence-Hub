"""
Critic Agent
Quality control for generated answers
"""

from typing import Literal
import logging

from .state import AgentState
from .prompts import get_critic_prompt

logger = logging.getLogger(__name__)


def critic_node(state: AgentState) -> AgentState:
    """
    Critic node - evaluates answer quality.

    Args:
        state: Current agent state

    Returns:
        Updated state with quality score and feedback
    """
    answer = state.final_answer
    query = state.query
    sources = state.sources

    if not answer:
        state.quality_score = 0.0
        state.needs_revision = True
        state.feedback = "Yanıt bulunmuyor."
        state.steps.append("Critic: Yanıt yok")
        return state

    score = 0.0
    feedback_parts = []

    if len(answer) < 50:
        score += 0.1
        feedback_parts.append("Yanıt çok kısa")
    else:
        score += 0.3

    if sources:
        score += 0.2
    else:
        feedback_parts.append("Kaynak belirtilmemiş")

    if "bilgi bulunamadı" not in answer.lower() and "üzgünüm" not in answer.lower():
        score += 0.3
    else:
        score += 0.1

    questionable_phrases = ["kesinlikle", "mutlaka", "her zaman", "hiçbir zaman", " kesin ", "假的"]
    has_hallucination = any(p in answer.lower() for p in questionable_phrases)

    if not has_hallucination:
        score += 0.2
    else:
        feedback_parts.append("Belki hallucination içeren ifadeler var")

    state.quality_score = min(score, 1.0)
    state.needs_revision = score < 0.5
    state.feedback = "; ".join(feedback_parts) if feedback_parts else "Kalite kontrolü geçti"

    state.steps.append(f"Critic: Puan={state.quality_score:.2f}, Revizyon={state.needs_revision}")

    return state


def should_revision(state: AgentState) -> Literal["writer", "critic"]:
    """
    Determine if answer needs revision.

    Args:
        state: Current state

    Returns:
        Next node
    """
    if state.needs_revision:
        return "writer"
    return "critic"
