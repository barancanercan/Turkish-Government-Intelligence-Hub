"""
Agent Tools
Reusable tools for LangGraph agents
"""

from typing import List, Dict, Any, Optional, TypedDict
from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import logging
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src import config
from src.core.parties import normalize_party_name
from src.core.duckduckgo_search import search_web

logger = logging.getLogger(__name__)


wikipedia_api = WikipediaAPIWrapper(lang="en", top_k_results=3, doc_content_chars_max=1500)
wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia_api)


@tool
def search_wikipedia(query: str) -> str:
    """
    Wikipedia'dan bilgi arar. Türk siyasi figürler, partiler ve konular hakkında bilgi almak için kullanılır.

    Args:
        query: Arama sorgusu

    Returns:
        Wikipedia araştırma sonuçları
    """
    try:
        tr_query = (
            query.replace("ı", "i")
            .replace("ş", "s")
            .replace("ç", "c")
            .replace("ğ", "g")
            .replace("ü", "u")
            .replace("ö", "o")
        )

        try:
            result = wikipedia_tool.invoke(tr_query)
            if result and "No good Wikipedia Search Result" not in result:
                return result
        except:
            pass

        try:
            result = wikipedia_tool.invoke(query)
            return result
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            return "Wikipedia'da bilgi bulunamadı."
    except Exception as e:
        logger.error(f"Wikipedia search error: {e}")
        return "Wikipedia'da bilgi bulunamadı."


class VectorStoreWrapper:
    """Wrapper for Chroma vector store."""

    def __init__(self, vectorstore: Chroma):
        self.vectorstore = vectorstore

    def search(self, query: str, party: Optional[str] = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search vector store.

        Args:
            query: Search query
            party: Optional party filter
            top_k: Number of results

        Returns:
            List of documents with metadata
        """
        filter_meta = {"party": normalize_party_name(party)} if party else None

        try:
            results = self.vectorstore.similarity_search_with_score(query, k=top_k, filter=filter_meta)

            docs = []
            for doc, score in results:
                docs.append(
                    {
                        "id": doc.metadata.get("id", "unknown"),
                        "content": doc.page_content,
                        "source": doc.metadata.get("source", "unknown"),
                        "party": doc.metadata.get("party", party),
                        "score": float(score),
                    }
                )

            return docs
        except Exception as e:
            logger.error(f"Vector store search error: {e}")
            return []


@tool
def retrieve_documents(query: str, party: Optional[str] = None, top_k: int = 5) -> str:
    """
    Retrieve relevant documents from the political document database.

    Args:
        query: The search query about political parties
        party: Optional party name to filter (e.g., 'CHP', 'AKP', 'MHP')
        top_k: Number of documents to retrieve (default 5)

    Returns:
        JSON string of retrieved documents with content and metadata
    """
    from src.core.cache import get_vectorstore

    try:
        vectorstore = get_vectorstore()
        wrapper = VectorStoreWrapper(vectorstore)
        results = wrapper.search(query, party, top_k)

        if not results:
            return "[]"

        import json

        return json.dumps(results, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Document retrieval error: {e}")
        return f"[]"


@tool
def search_web_tool(query: str, max_results: int = 5) -> str:
    """
    Search the web for current information about political parties.

    Args:
        query: Search query
        max_results: Maximum number of results (default 5)

    Returns:
        JSON string of search results with title, snippet, and url
    """
    try:
        results = search_web(query, max_results=max_results)

        formatted = []
        for r in results:
            url = getattr(r, "url", "")
            title = getattr(r, "title", "")
            snippet = getattr(r, "snippet", "")

            bad_patterns = [
                "buzz",
                "click",
                "tag",
                "category",
                "search?",
                "facebook",
                "twitter",
                "instagram",
                "youtube.com/watch",
                "tiktok",
            ]
            is_bad = any(p in url.lower() for p in bad_patterns)

            if not is_bad and len(url) > 20 and title:
                formatted.append(
                    {
                        "title": title,
                        "snippet": snippet[:300] if snippet else "",
                        "url": url,
                    }
                )

        import json

        return json.dumps(formatted, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Web search error: {e}")
        return "[]"


@tool
def analyze_comparison(party1_docs: str, party2_docs: str, topic: str) -> str:
    """
    Analyze and compare documents from two political parties on a specific topic.

    Args:
        party1_docs: JSON string of party 1 documents
        party2_docs: JSON string of party 2 documents
        topic: The topic to compare (e.g., 'economy', 'education')

    Returns:
        Comparison analysis text
    """
    import json

    try:
        p1 = json.loads(party1_docs) if party1_docs else []
        p2 = json.loads(party2_docs) if party2_docs else []

        analysis = f"Karşılaştırma: {topic}\n\n"
        analysis += f"Parti 1 ({p1[0].get('party', 'N/A') if p1 else 'N/A'}):\n"
        for doc in p1[:3]:
            analysis += f"- {doc.get('content', '')[:200]}...\n\n"

        analysis += f"Parti 2 ({p2[0].get('party', 'N/A') if p2 else 'N/A'}):\n"
        for doc in p2[:3]:
            analysis += f"- {doc.get('content', '')[:200]}...\n\n"

        return analysis

    except Exception as e:
        logger.error(f"Comparison analysis error: {e}")
        return "Karşılaştırma yapılamadı."


def get_tools() -> List[Any]:
    """
    Get all tools for agents.

    Returns:
        List of LangChain tools
    """
    return [
        retrieve_documents,
        search_web_tool,
        search_wikipedia,
        analyze_comparison,
    ]
