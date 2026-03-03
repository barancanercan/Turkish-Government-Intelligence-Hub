"""
Context Grader Agent
Retrieval sonuçlarını değerlendirir ve alakasız olanları filtreler.
"""

from typing import List, Tuple
from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)


class ContextGrader:
    """Belge alakalılık değerlendirici."""

    RELEVANCE_THRESHOLD = 0.3

    def __init__(self, llm=None):
        self.llm = llm

    def grade_document(self, question: str, document: Document) -> float:
        """
        Tek bir belgenin soruya alakalılığını değerlendir.

        Returns:
            float: 0-1 arası alakalılık skoru
        """
        content = document.page_content[:500]  # İlk 500 karakter
        party = document.metadata.get("party", "unknown")

        # Basit keyword-based grading (LLM olmadan hızlı)
        question_lower = question.lower()
        content_lower = content.lower()

        score = 0.0

        # Parti eşleşmesi
        if party.lower() in question_lower:
            score += 0.4

        # Keyword eşleşmeleri
        question_words = set(question_lower.split())
        content_words = set(content_lower.split())
        common_words = question_words.intersection(content_words)

        # Stop words çıkar
        stop_words = {"bir", "ve", "ile", "icin", "bu", "da", "de", "mi", "mu", "ne", "nedir", "nasil", "kimdir"}
        meaningful_common = common_words - stop_words

        if meaningful_common:
            score += min(0.4, len(meaningful_common) * 0.1)

        # Soru tipi eşleşmesi
        if "kimdir" in question_lower and any(w in content_lower for w in ["baskan", "genel baskan", "lider"]):
            score += 0.2
        elif "nedir" in question_lower and any(w in content_lower for w in ["tanim", "amac", "ilke"]):
            score += 0.2

        return min(1.0, score)

    def filter_documents(
        self,
        question: str,
        documents: List[Document],
        threshold: float = None
    ) -> Tuple[List[Document], List[float]]:
        """
        Belgeleri filtrele ve skorlarını döndür.

        Returns:
            Tuple[List[Document], List[float]]: (filtrelenmiş belgeler, skorlar)
        """
        if threshold is None:
            threshold = self.RELEVANCE_THRESHOLD

        scored_docs = []
        for doc in documents:
            score = self.grade_document(question, doc)
            if score >= threshold:
                scored_docs.append((doc, score))
                logger.debug(f"PASS [{score:.2f}]: {doc.metadata.get('party', '?')} - {doc.page_content[:50]}...")
            else:
                logger.debug(f"FAIL [{score:.2f}]: {doc.metadata.get('party', '?')} - {doc.page_content[:50]}...")

        # Skora göre sırala
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        if not scored_docs:
            # Hiç belge geçemediyse en yüksek skorlu 2 tanesini al
            all_scored = [(doc, self.grade_document(question, doc)) for doc in documents]
            all_scored.sort(key=lambda x: x[1], reverse=True)
            scored_docs = all_scored[:2]
            logger.warning("No docs passed threshold, using top 2")

        filtered_docs = [doc for doc, _ in scored_docs]
        scores = [score for _, score in scored_docs]

        return filtered_docs, scores


# Singleton instance
_grader_instance = None

def get_context_grader() -> ContextGrader:
    global _grader_instance
    if _grader_instance is None:
        _grader_instance = ContextGrader()
    return _grader_instance
