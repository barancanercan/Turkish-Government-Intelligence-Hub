"""
Writer Agent
Generates final answer from retrieved information
"""

from typing import Optional
import logging

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .state import AgentState
from .prompts import get_writer_prompt
from .researcher import get_retrieved_context, get_web_context, get_wikipedia_context

logger = logging.getLogger(__name__)


def writer_node(state: AgentState, llm) -> AgentState:
    """
    Writer node - generates final answer.

    Args:
        state: Current agent state
        llm: Language model for generation

    Returns:
        Updated state with final answer
    """
    query = state.query
    context = get_retrieved_context(state)
    web_context = get_web_context(state)
    wiki_context = get_wikipedia_context(state)

    has_any_info = bool(context or web_context or wiki_context or state.wikipedia_results or state.web_results)

    logger.info(
        f"Writer check - context: {bool(context)}, web: {bool(web_context)}, wiki: {bool(wiki_context)}, wiki_results: {bool(state.wikipedia_results)}"
    )

    if not has_any_info:
        state.final_answer = "Üzgünüm, bu konuda yeterli bilgi bulamadım."
        state.steps.append("Writer: Bilgi bulunamadı")
        return state

    try:
        from langchain_ollama import OllamaLLM
        from src import config

        llm_to_use = None

        if isinstance(llm, tuple):
            llm = llm[0]

        if hasattr(llm, "first") and hasattr(llm.first, "model"):
            llm_to_use = llm.first
        elif hasattr(llm, "model"):
            llm_to_use = llm
        else:
            llm_to_use = OllamaLLM(
                model=config.LLM_MODEL,
                temperature=config.LLM_TEMPERATURE,
                base_url="http://localhost:11434",
                num_predict=config.LLM_MAX_TOKENS,
            )

        web_info = ""
        if state.web_results:
            for w in state.web_results[:3]:
                web_info += (
                    f"- {w.get('title', 'N/A')}: {w.get('snippet', 'N/A')[:200]}... (Kaynak: {w.get('url', 'N/A')})\n"
                )

        wiki_info = ""
        if state.wikipedia_results:
            for w in state.wikipedia_results:
                content = w.get("content", "") or w.get("extract", "")
                if content:
                    wiki_info += f"- {content[:800]}\n\n"

        full_prompt = f"""Sen MİZAN-AI'nın Writer Agent'ısın. Türk siyasi partiler hakkında soruları yanıtlamakla görevlisin.

Soru: {query}

Yerel Veritabanı Bilgileri:
{context if context else "Yerel veritabanında bilgi bulunamadı"}

Web Araştırma Sonuçları:
{web_info if web_info else "Web araması yapılmadı veya sonuç bulunamadı"}

Wikipedia Araştırma Sonuçları:
{wiki_info if wiki_info else "Wikipedia'da bilgi bulunamadı"}

Görevin:
1. Yukarıdaki bilgileri kullanarak soruyu yanıtla
2. TÜRKÇE yanıt ver - BAŞKA DİL KULLANMA
3. Wikipedia'dan gelen bilgileri ÖNCELİKLİ olarak kullan
4. Kaynakları mutlaka belirt
5. Kısa ve öz ol (maksimum 3 paragraf)
6. Tarafsız ve nesnel ol
7. Yanıtın sonunda "Kaynaklar:" kısmında kaynakları listele
8. Eğer bilgi varsa detaylı yanıt ver, yoksa bilgi bulunamadığını söyle

Yanıt:"""

        answer = llm_to_use.invoke(full_prompt)

        if not isinstance(answer, str):
            answer = str(answer) if answer else "Yanıt alınamadı"

        if state.web_results:
            web_sources = [w.get("url", "") for w in state.web_results[:3] if w.get("url")]
            state.sources = list(set(state.sources + web_sources))

        state.final_answer = answer
        state.draft_answer = answer

    except Exception as e:
        logger.error(f"Writer error: {e}")
        state.final_answer = f"Yanıt oluşturulurken hata: {str(e)}"
        state.draft_answer = state.final_answer

    sources = list(set([d.source for d in state.retrieved_docs if d.source]))
    state.sources = sources
    state.citations = [s for s in sources if s]

    state.steps.append("Writer: Yanıt oluşturuldu")

    return state


def f_web(state: AgentState) -> str:
    """Get web context for prompt."""
    return get_web_context(state) if state.web_results else ""
