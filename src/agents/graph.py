"""
LangGraph Workflow Definitions
Multi-agent orchestration for MIZAN-AI
"""

from typing import Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import logging

from .state import AgentState, create_initial_state
from .supervisor import supervisor_node, classify_query, should_continue_supervisor
from .researcher import researcher_node
from .analyst import analyst_node
from .writer import writer_node
from .critic import critic_node, should_revision

logger = logging.getLogger(__name__)


def create_workflow(llm) -> StateGraph:
    """
    Create LangGraph workflow for multi-agent system.

    Args:
        llm: Language model instance

    Returns:
        Compiled StateGraph
    """

    workflow = StateGraph(AgentState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("writer", lambda state: writer_node(state, llm))
    workflow.add_node("critic", critic_node)

    workflow.set_entry_point("supervisor")

    workflow.add_conditional_edges(
        "supervisor",
        should_continue_supervisor,
        {
            "analyst": "analyst",
            "researcher": "researcher",
        },
    )

    workflow.add_edge("researcher", "writer")
    workflow.add_edge("analyst", "writer")
    workflow.add_edge("writer", "critic")
    workflow.add_edge("critic", END)

    checkpointer = MemorySaver()

    return workflow.compile(checkpointer=checkpointer)


def run_query(query: str, llm, config: Optional[Dict[str, Any]] = None) -> AgentState:
    """
    Run query through multi-agent workflow.

    Args:
        query: User question
        llm: Language model
        config: Optional configuration

    Returns:
        Final agent state with answer
    """
    initial_state = create_initial_state(query)

    graph = create_workflow(llm)

    config = config or {"configurable": {"thread_id": "default"}}

    try:
        result = graph.invoke(initial_state, config=config)

        if isinstance(result, dict):
            final_state = AgentState(**result)
        else:
            final_state = result

        return final_state
    except Exception as e:
        logger.error(f"Workflow error: {e}")
        initial_state.error = str(e)
        initial_state.final_answer = f"Sistem hatasi: {str(e)}"
        return initial_state


def run_simple_query(query: str, llm) -> str:
    """
    Simple query execution - returns only the answer.

    Args:
        query: User question
        llm: Language model

    Returns:
        Final answer string
    """
    state = run_query(query, llm)
    return state.final_answer


class AgentWorkflow:
    """
    Wrapper class for LangGraph workflow.
    Provides easy-to-use interface for the multi-agent system.
    """

    def __init__(self, llm):
        """
        Initialize workflow.

        Args:
            llm: Language model instance
        """
        self.llm = llm
        self.graph = create_workflow(llm)

    def query(self, question: str, thread_id: str = "default") -> Dict[str, Any]:
        """
        Execute a query through the agent workflow.

        Args:
            question: User question
            thread_id: Thread ID for conversation continuity

        Returns:
            Dictionary with answer and metadata
        """
        initial_state = create_initial_state(question)
        config = {"configurable": {"thread_id": thread_id}}

        final_state = self.graph.invoke(initial_state, config=config)

        return {
            "answer": final_state.get("final_answer", ""),
            "sources": final_state.get("sources", []),
            "quality_score": final_state.get("quality_score", 0.0),
            "steps": final_state.get("steps", []),
            "query_type": final_state.get("query_type", {}).type if final_state.get("query_type") else "unknown",
            "needs_revision": final_state.get("needs_revision", False),
        }

    def compare(self, question: str, parties: list, thread_id: str = "default") -> Dict[str, Any]:
        """
        Execute a comparison query.

        Args:
            question: Comparison question
            parties: List of parties to compare
            thread_id: Thread ID

        Returns:
            Dictionary with comparison and metadata
        """
        state = create_initial_state(question)

        from .supervisor import extract_parties
        from .state import QueryType

        parties_found = extract_parties(question)
        if not parties_found and parties:
            parties_found = parties

        state.query_type = QueryType(type="comparison", parties=parties_found, confidence=0.9)

        config = {"configurable": {"thread_id": thread_id}}
        final_state = self.graph.invoke(state, config=config)

        return {
            "answer": final_state.final_answer,
            "comparison": final_state.comparison,
            "sources": final_state.sources,
            "quality_score": final_state.quality_score,
        }
