"""
Researcher Agent
Retrieves documents from vector store, web and Wikipedia
"""

from typing import List, Dict, Any
import json
import logging

from .state import AgentState, DocumentInfo
from .prompts import get_researcher_prompt
from .tools import retrieve_documents, search_web_tool, search_wikipedia

logger = logging.getLogger(__name__)


def researcher_node(state: AgentState) -> AgentState:
    """
    Researcher node - retrieves relevant documents.

    Args:
        state: Current agent state

    Returns:
        Updated state with retrieved documents
    """
    query = state.query
    parties = state.query_type.parties if state.query_type else []

    retrieved_docs = []
    web_results = []
    wikipedia_results = []

    if parties:
        for party in parties:
            docs = retrieve_documents.invoke({"query": query, "party": party, "top_k": 5})

            if docs and docs != "[]":
                try:
                    parsed = json.loads(docs)
                    for d in parsed:
                        doc_info = DocumentInfo(
                            id=d.get("id", ""),
                            content=d.get("content", ""),
                            source=d.get("source", ""),
                            party=d.get("party", party),
                            score=d.get("score", 0.0),
                        )
                        retrieved_docs.append(doc_info)
                except json.JSONDecodeError:
                    pass

    has_kişi = any(
        kw in query.lower()
        for kw in ["kimdir", "kim", "başkan", "lider", "başkanı", "kaç", "ne zaman", "nereli", "doğum"]
    )
    has_nasıl = any(kw in query.lower() for kw in ["nasıl", "nerede", "nedir", "tarihçe", "biyografi"])
    needs_web = has_kişi or has_nasıl or not retrieved_docs

    if needs_web:
        web_result = search_web_tool.invoke({"query": query, "max_results": 3})

        if web_result and web_result != "[]":
            try:
                web_results = json.loads(web_result)
            except json.JSONDecodeError:
                pass

    has_wikipedia = any(
        kw in query.lower()
        for kw in ["kimdir", "kim", "başkan", "lider", "parti", "tarih", "kuruluş", "nereli", "doğum", "biyografi"]
    )
    if has_wikipedia or needs_web or not retrieved_docs:
        wiki_result = search_wikipedia.invoke({"query": query})

        logger.info(f"Wikipedia result length: {len(wiki_result) if wiki_result else 0}")

        if wiki_result and "bulunamadı" not in wiki_result.lower() and "no good" not in wiki_result.lower():
            wikipedia_results = [{"content": wiki_result, "source": "Wikipedia"}]
            logger.info("Wikipedia result stored successfully")

    state.retrieved_docs = retrieved_docs
    state.web_results = web_results
    state.wikipedia_results = wikipedia_results
    state.sources = [d.source for d in retrieved_docs if d.source]

    state.steps.append(
        f"Researcher: {len(retrieved_docs)} doküman, {len(web_results)} web, {len(wikipedia_results)} wikipedia sonucu"
    )

    return state


def get_retrieved_context(state: AgentState) -> str:
    """
    Get context string from retrieved documents.

    Args:
        state: Current state

    Returns:
        Context string
    """
    context_parts = []

    for doc in state.retrieved_docs[:5]:
        context_parts.append(f"[{doc.party or doc.source}]\n{doc.content[:500]}")

    return "\n\n".join(context_parts)


def get_web_context(state: AgentState) -> str:
    """
    Get context string from web results.

    Args:
        state: Current state

    Returns:
        Web context string
    """
    if not state.web_results:
        return ""

    parts = ["WEB SONUÇLARI:\n"]
    for r in state.web_results:
        parts.append(f"- {r.get('title', '')}: {r.get('snippet', '')}")

    return "\n".join(parts)


def get_wikipedia_context(state: AgentState) -> str:
    """
    Get context string from Wikipedia results.

    Args:
        state: Current state

    Returns:
        Wikipedia context string
    """
    if not state.wikipedia_results:
        return ""

    parts = ["WIKIPEDIA SONUÇLARI:\n"]
    for r in state.wikipedia_results:
        content = r.get("content", "") or r.get("extract", "")
        if content:
            parts.append(f"- {content[:500]}")

    return "\n".join(parts)
