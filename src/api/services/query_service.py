"""
Query Service
Business logic for query processing - Full Streamlit Pipeline Integration
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class QueryService:
    """
    Service for processing queries using the full Streamlit pipeline.
    Includes: Content filtering, Query analysis, Local search, Intent analysis,
    Web search, Wikipedia, and Answer synthesis.
    """

    def __init__(self):
        self.vectorstore = None
        self.llm = None
        self.llm_type = None

    def _ensure_initialized(self, party: str = "CHP"):
        """Lazy initialization of vectorstore and LLM."""
        if self.vectorstore is None:
            from src.core.cache import get_vectorstore
            self.vectorstore = get_vectorstore()

        if self.llm is None:
            from src.core.llm_setup import create_llm_handler
            self.llm, self.llm_type = create_llm_handler(party)

    async def process_query(
        self,
        question: str,
        party: Optional[str] = None,
        top_k: int = 5,
        user_id: str = "anonymous",
    ) -> Dict[str, Any]:
        """
        Process a query using the improved pipeline with Search Synthesizer.

        Pipeline:
        1. Party detection from query (not from UI selection!)
        2. Content filtering
        3. Query analysis (sub-questions)
        4. Local knowledge search (with correct party)
        5. Web search decision
        6. Web search with correct party queries
        7. Search result synthesis (extract facts, filter irrelevant)
        8. Answer generation with synthesized context
        """
        try:
            from src.core.search_synthesizer_agent import get_search_synthesizer
            from src.core.search_agent import create_search_agent
            from src.core.query_analyzer import get_query_analyzer
            from src.core.content_filter import should_answer
            from src.core.cache import get_vectorstore
            from src.core.parties import normalize_party_name
            from src import config

            # 1. ÖNCE SORGUDAN PARTİ TESPİT ET!
            synthesizer = get_search_synthesizer()
            detected_party = synthesizer.extract_party_from_query(question)

            if detected_party:
                target_party = detected_party
                logger.info(f"Sorgudan parti tespit edildi: {target_party}")
            else:
                target_party = normalize_party_name(party) if party else "CHP"
                logger.info(f"Default parti kullanılıyor: {target_party}")

            # 2. Content filtering
            should_respond, filter_message = should_answer(question)
            if not should_respond:
                return {
                    "answer": filter_message,
                    "sources": [],
                    "citations": [],
                    "query_type": "filtered",
                }

            # 3. Query analysis
            query_analyzer = get_query_analyzer()
            query_analysis = query_analyzer.analyze(question, target_party)

            needs_web = any(sq.requires_web for sq in query_analysis.sub_questions)
            logger.info(f"Query analysis: {len(query_analysis.sub_questions)} alt soru, web_needed={needs_web}")

            # 4. Initialize LLM with correct party
            self._ensure_initialized(target_party)

            # 5. Local knowledge search with CORRECT party
            vectorstore = get_vectorstore()
            filter_meta = {"party": target_party}
            docs = vectorstore.similarity_search(question, k=top_k, filter=filter_meta)

            local_context = ""
            local_sources = []
            if docs:
                local_context = "\n\n".join([
                    f"[{doc.metadata.get('party', target_party)}]: {doc.page_content[:500]}"
                    for doc in docs[:3]
                ])
                local_sources = [doc.metadata.get("source", "") for doc in docs]
                logger.info(f"Local search: {len(docs)} doküman bulundu ({target_party})")

            # 6. Web search with CORRECT party
            web_context = ""
            web_sources = []

            if needs_web or not docs:
                logger.info(f"Web araması başlatılıyor: {target_party}")
                search_agent = create_search_agent()
                search_result = search_agent.search(question, target_party)

                if search_result.has_results:
                    # 7. SYNTHESIZE web results - extract facts, filter noise
                    synth_context = synthesizer.synthesize(
                        search_result.results,
                        question,
                        target_party
                    )

                    web_context = synth_context.to_prompt_context()
                    web_sources = synth_context.sources
                    logger.info(f"Web synthesis: {len(synth_context.extracted_facts)} fact çıkarıldı")

            # 8. Generate answer with proper context
            full_context = ""
            if local_context:
                full_context += f"[YEREL BELGELER - {target_party} Tüzüğü]:\n{local_context}\n\n"
            if web_context:
                full_context += f"{web_context}\n\n"

            # Build prompt
            system_prompt = f"""Sen {target_party} hakkında uzman bir asistansın.

GÖREV: Aşağıdaki soruyu yanıtla.
KURALLAR:
1. Önce web araştırma sonuçlarını kullan (güncel bilgi)
2. Sonra yerel belgelerden destekle
3. Her bilgi için kaynak belirt
4. Türkçe yanıt ver
5. Bilgi bulunamadıysa açıkça belirt

BAĞLAM:
{full_context}

SORU: {question}

YANIT:"""

            # Invoke LLM
            from langchain_ollama import OllamaLLM
            direct_llm = OllamaLLM(
                model=config.LLM_MODEL,
                temperature=config.LLM_TEMPERATURE,
                base_url="http://localhost:11434",
            )

            answer = str(direct_llm.invoke(system_prompt))

            all_sources = list(set(local_sources + web_sources))
            query_type = "web" if web_context else "local"

            logger.info(f"Query completed: party={target_party}, type={query_type}, sources={len(all_sources)}")

            return {
                "answer": answer,
                "sources": all_sources,
                "citations": all_sources,
                "query_type": query_type,
                "web_search_used": bool(web_context),
                "detected_party": target_party,
            }

        except Exception as e:
            logger.error(f"Query processing error: {e}", exc_info=True)
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
        Process a comparison query using full pipeline for each party.
        """
        try:
            from src.query_system import search_local_knowledge
            from src.core.parties import normalize_party_name
            from src.core.cache import get_vectorstore
            from src.core.llm_setup import create_llm_handler
            vectorstore = get_vectorstore()
            llm, llm_type = create_llm_handler(parties[0])

            party_positions = {}
            all_sources = []

            for party in parties:
                normalized = normalize_party_name(party)

                # Full pipeline search for each party
                local_context, docs, scores = search_local_knowledge(
                    vectorstore, question, normalized, top_k
                )

                party_positions[normalized] = local_context[:800] if local_context else "Bilgi bulunamadı"
                all_sources.extend([doc.metadata.get("source", "") for doc in docs])

            # Build comparison prompt
            party_contexts = "\n\n".join([
                f"=== {p} ===\n{pos}" for p, pos in party_positions.items()
            ])

            comparison_prompt = f"""Sen Türk siyasi partileri uzmanısın. Aşağıdaki parti belgelerini karşılaştır.

SORU: {question}

PARTİ BİLGİLERİ:
{party_contexts}

GÖREV:
1. Her partinin bu konudaki yaklaşımını özetle
2. Benzerlik ve farklılıkları belirt
3. Türkçe ve tarafsız yanıt ver
4. Kaynaklara atıfta bulun

KARŞILAŞTIRMALI YANIT:"""

            # Get LLM for direct invoke
            from langchain_ollama import OllamaLLM
            from src import config

            direct_llm = OllamaLLM(
                model=config.LLM_MODEL,
                temperature=config.LLM_TEMPERATURE,
                base_url="http://localhost:11434",
            )

            response = direct_llm.invoke(comparison_prompt)
            comparison = str(response)

            return {
                "comparison": comparison,
                "party_positions": party_positions,
                "sources": list(set(all_sources)),
            }

        except Exception as e:
            logger.error(f"Comparison error: {e}", exc_info=True)
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
