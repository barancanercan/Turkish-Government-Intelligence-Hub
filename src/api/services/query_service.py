"""
Query Service
Business logic for query processing
"""

from typing import Dict, Any, List, Optional
import logging
from src.core.reasoning import enhance_query_with_reasoning
from src.agents.grader import get_context_grader
from src.core.search_agent import SearchAgent

logger = logging.getLogger(__name__)

# Web search instance
_search_agent = None

def get_search_agent() -> SearchAgent:
    global _search_agent
    if _search_agent is None:
        _search_agent = SearchAgent()
    return _search_agent


class QueryService:
    """
    Service for processing queries.
    """

    def __init__(self):
        self.vectorstore = None
        self.llm = None

    async def process_query(
        self,
        question: str,
        party: Optional[str] = None,
        top_k: int = 5,
        user_id: str = "anonymous",
    ) -> Dict[str, Any]:
        """
        Process a simple query.
        """
        try:
            from src.core.cache import get_vectorstore
            from src.core.llm_setup import create_llm_handler
            from src import config

            if not self.vectorstore:
                self.vectorstore = get_vectorstore()

            if not self.llm:
                self.llm, _ = create_llm_handler(party or "CHP")

            filter_meta = {"party": party.upper()} if party else None

            docs = self.vectorstore.similarity_search(question, k=top_k, filter=filter_meta)

            # Grader ile alakalı belgeleri filtrele
            grader = get_context_grader()
            filtered_docs, scores = grader.filter_documents(question, docs)

            logger.info(f"Retrieved {len(docs)} docs, filtered to {len(filtered_docs)} relevant docs")

            # Context'i daha iyi formatla
            context_parts = []
            for i, doc in enumerate(filtered_docs):
                party = doc.metadata.get("party", "Bilinmiyor")
                score = scores[i] if i < len(scores) else 0.0
                context_parts.append(f"[Kaynak {i+1} - {party}] (Relevans: {score:.2f}):\n{doc.page_content}")
            context = "\n\n".join(context_parts)

            # Chain-of-Thought reasoning ile query'yi zenginlestir
            enhanced_prompt, reasoning_analysis = enhance_query_with_reasoning(question, context)

            # "kimdir" sorularinda veya PERSON_INFO tipinde web search yap
            web_context = ""
            web_sources = []
            if reasoning_analysis.get("type") == "PERSON_INFO" or "kimdir" in question.lower():
                try:
                    search_agent = get_search_agent()
                    search_result = search_agent.search(question)
                    if search_result.has_results:
                        web_context = f"\n\n[WEB ARAMA SONUCLARI]:\n{search_result.formatted_text}"
                        web_sources = [r.url for r in search_result.results[:3]]
                        logger.info(f"Web search returned {len(search_result.results)} results")
                except Exception as e:
                    logger.warning(f"Web search failed: {e}")

            # Web context'i ekle
            if web_context:
                enhanced_prompt = enhanced_prompt.replace(
                    "KAYNAK BILGI:",
                    f"KAYNAK BILGI:{web_context}\n\n[YEREL BELGELER]:"
                )

            # Chain expects dict with 'context' and 'question'
            response = self.llm.invoke({"question": enhanced_prompt, "context": ""})
            if hasattr(response, "content"):
                answer = response.content
            elif hasattr(response, "text"):
                answer = response.text
            else:
                answer = str(response)

            sources = list(set([doc.metadata.get("source", "unknown") for doc in filtered_docs]))
            # Web kaynaklarini ekle
            all_sources = sources + web_sources

            return {
                "answer": answer,
                "sources": all_sources,
                "citations": all_sources,
                "query_type": reasoning_analysis.get("type", "simple"),
                "reasoning_analysis": reasoning_analysis,
                "web_search_used": len(web_sources) > 0,
            }

        except Exception as e:
            logger.error(f"Query processing error: {e}")
            return {
                "answer": f"Hata: {str(e)}",
                "sources": [],
                "citations": [],
                "query_type": "error",
            }

    async def process_comparison(
        self,
        question: str,
        parties: List[str],
        top_k: int = 5,
        user_id: str = "anonymous",
    ) -> Dict[str, Any]:
        """
        Process a comparison query.
        """
        try:
            from src.core.cache import get_vectorstore
            from src.core.llm_setup import create_llm_handler

            vectorstore = get_vectorstore()
            llm, _ = create_llm_handler(parties[0])
            grader = get_context_grader()

            party_positions = {}
            all_sources = []

            for party in parties:
                docs = vectorstore.similarity_search(question, k=top_k, filter={"party": party})

                # Grader ile alakalı belgeleri filtrele
                filtered_docs, scores = grader.filter_documents(question, docs)
                logger.info(f"Party {party}: Retrieved {len(docs)} docs, filtered to {len(filtered_docs)} relevant")

                context = "\n\n".join([doc.page_content for doc in filtered_docs])
                party_positions[party] = context[:500]

                all_sources.extend([doc.metadata.get("source", "") for doc in filtered_docs])

            comparison_prompt = f"""Karşılaştırma sorusu: {question}

{chr(10).join([f"{p}: {pos}" for p, pos in party_positions.items()])}

Türkçe olarak karşılaştırmalı yanıt ver:"""

            # For comparison, create a direct prompt without using the chain
            # Get the LLM directly from the chain's middle
            actual_llm = None
            if hasattr(llm, "middle") and llm.middle:
                actual_llm = llm.middle[0]
            elif hasattr(llm, "last"):
                actual_llm = llm

            if actual_llm is None:
                actual_llm = llm

            response = actual_llm.invoke(comparison_prompt)
            comparison = response.content if hasattr(response, "content") else str(response)

            return {
                "comparison": comparison,
                "party_positions": party_positions,
                "sources": list(set(all_sources)),
            }

        except Exception as e:
            logger.error(f"Comparison error: {e}")
            return {
                "comparison": f"Hata: {str(e)}",
                "party_positions": {},
                "sources": [],
            }

    async def process_analysis(
        self,
        question: str,
        parties: Optional[List[str]] = None,
        include_web: bool = True,
        user_id: str = "anonymous",
    ) -> Dict[str, Any]:
        """
        Process a deep analysis query.
        """
        result = await self.process_query(question, party=parties[0] if parties else None)

        web_results = []
        if include_web:
            try:
                from src.core.duckduckgo_search import search_web

                web_results = search_web(question, max_results=3)
            except Exception as e:
                logger.error(f"Web search error: {e}")

        return {
            "analysis": result.get("answer", ""),
            "key_findings": [],
            "sources": result.get("sources", []),
            "web_results": web_results,
        }
