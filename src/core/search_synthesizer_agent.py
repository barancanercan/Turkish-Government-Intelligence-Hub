"""
Search Synthesizer Agent
Arama sonuçlarından bilgi çıkarır, özetler ve kaynak belirterek ana modeli besler.
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ExtractedInfo:
    """Arama sonucundan çıkarılan bilgi."""
    fact: str
    source_title: str
    source_url: str
    confidence: float = 0.8

    def to_context(self) -> str:
        return f"- {self.fact} (Kaynak: {self.source_title})"


@dataclass
class SynthesizedContext:
    """Sentezlenmiş arama context'i."""
    summary: str
    extracted_facts: List[ExtractedInfo] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    party: Optional[str] = None
    query_type: str = "general"

    def to_prompt_context(self) -> str:
        """Ana model için context formatı."""
        if not self.extracted_facts:
            return ""

        lines = [f"[WEB ARAŞTIRMA SONUÇLARI - {self.party or 'Genel'}]"]
        lines.append("")

        for fact in self.extracted_facts:
            lines.append(fact.to_context())

        lines.append("")
        lines.append(f"Özet: {self.summary}")

        return "\n".join(lines)


class SearchSynthesizerAgent:
    """
    Arama sonuçlarını analiz eder, alakalı bilgileri çıkarır ve özetler.
    """

    # Parti liderleri (güncel bilgi)
    PARTY_LEADERS = {
        "AKP": {"leader": "Recep Tayyip Erdoğan", "title": "Genel Başkan ve Cumhurbaşkanı"},
        "CHP": {"leader": "Özgür Özel", "title": "Genel Başkan"},
        "MHP": {"leader": "Devlet Bahçeli", "title": "Genel Başkan"},
        "İYİ": {"leader": "Müsavat Dervişoğlu", "title": "Genel Başkan"},
        "DEM": {"leader": "Tuncer Bakırhan, Tülay Hatimoğulları", "title": "Eş Genel Başkanlar"},
        "SP": {"leader": "Temel Karamollaoğlu", "title": "Genel Başkan"},
        "ZP": {"leader": "Ümit Özdağ", "title": "Genel Başkan"},
        "BBP": {"leader": "Mustafa Destici", "title": "Genel Başkan"},
    }

    # Alakasız içerik filtreleri
    IRRELEVANT_PATTERNS = [
        "belediye başkanı kim",
        "il başkanı",
        "ilçe başkanı",
        "gençlik kolları",
        "kadın kolları",
        "eski genel başkan",
        "aday",
        "istifa",
    ]

    def __init__(self, llm=None):
        self.llm = llm

    def extract_party_from_query(self, query: str) -> Optional[str]:
        """Sorgudan parti ismini çıkar."""
        query_upper = query.upper()

        # Direkt parti kodu kontrolü
        party_codes = ["AKP", "CHP", "MHP", "İYİ", "IYI", "DEM", "SP", "ZP", "BBP"]
        for code in party_codes:
            if code in query_upper:
                return "İYİ" if code == "IYI" else code

        # Uzun isim kontrolü
        party_names = {
            "ADALET VE KALKINMA": "AKP",
            "AK PARTİ": "AKP",
            "AK PARTI": "AKP",
            "CUMHURİYET HALK": "CHP",
            "CUMHURIYET HALK": "CHP",
            "MİLLİYETÇİ HAREKET": "MHP",
            "MILLIYETCI HAREKET": "MHP",
            "İYİ PARTİ": "İYİ",
            "IYI PARTI": "İYİ",
            "HALKLARIN EŞİTLİK": "DEM",
            "SAADET": "SP",
            "ZAFER": "ZP",
            "BÜYÜK BİRLİK": "BBP",
        }

        for name, code in party_names.items():
            if name in query_upper:
                return code

        return None

    def get_known_leader(self, party: str) -> Optional[Dict[str, str]]:
        """Bilinen parti liderini döndür."""
        return self.PARTY_LEADERS.get(party.upper())

    def is_relevant_result(self, result: Any, party: str, query: str) -> bool:
        """Arama sonucunun alakalı olup olmadığını kontrol et."""
        title = getattr(result, 'title', '').lower()
        snippet = getattr(result, 'snippet', '').lower()
        content = f"{title} {snippet}"

        # Alakasız pattern kontrolü
        for pattern in self.IRRELEVANT_PATTERNS:
            if pattern in content and "genel başkan" not in query.lower():
                return False

        # Parti ismi veya kodu içermeli
        party_terms = [party.lower()]
        if party == "AKP":
            party_terms.extend(["ak parti", "akp", "adalet ve kalkınma"])
        elif party == "CHP":
            party_terms.extend(["chp", "cumhuriyet halk"])
        elif party == "MHP":
            party_terms.extend(["mhp", "milliyetçi hareket"])

        return any(term in content for term in party_terms)

    def extract_facts_from_results(
        self,
        results: List[Any],
        party: str,
        query: str
    ) -> List[ExtractedInfo]:
        """Arama sonuçlarından gerçekleri çıkar."""
        facts = []

        # Önce bilinen bilgiyi ekle
        known = self.get_known_leader(party)
        if known and any(kw in query.lower() for kw in ["kimdir", "kim", "başkan", "lider"]):
            facts.append(ExtractedInfo(
                fact=f"{party} {known['title']}: {known['leader']}",
                source_title="Güncel Bilgi",
                source_url="",
                confidence=1.0,
            ))

        # Alakalı sonuçlardan bilgi çıkar
        for result in results:
            if not self.is_relevant_result(result, party, query):
                continue

            title = getattr(result, 'title', '')
            snippet = getattr(result, 'snippet', '')
            url = getattr(result, 'url', '')

            # Snippet'ten anlamlı bilgi çıkar
            if snippet and len(snippet) > 50:
                # İlk cümleyi al
                first_sentence = snippet.split('.')[0].strip()
                if len(first_sentence) > 30:
                    facts.append(ExtractedInfo(
                        fact=first_sentence,
                        source_title=title[:50] if title else "Web",
                        source_url=url,
                        confidence=0.7,
                    ))

        return facts[:5]  # Max 5 fact

    def synthesize(
        self,
        results: List[Any],
        query: str,
        party: Optional[str] = None
    ) -> SynthesizedContext:
        """
        Arama sonuçlarını sentezle.

        Args:
            results: Web arama sonuçları
            query: Orijinal sorgu
            party: Hedef parti (opsiyonel, sorgudan çıkarılabilir)

        Returns:
            SynthesizedContext
        """
        # Parti tespiti
        detected_party = party or self.extract_party_from_query(query)

        if not detected_party:
            logger.warning(f"Parti tespit edilemedi: {query}")
            return SynthesizedContext(
                summary="Parti bilgisi tespit edilemedi.",
                party=None,
            )

        logger.info(f"SearchSynthesizer: Parti={detected_party}, Sonuç sayısı={len(results)}")

        # Bilgileri çıkar
        facts = self.extract_facts_from_results(results, detected_party, query)

        # Kaynakları topla
        sources = []
        for f in facts:
            if f.source_url and f.source_url not in sources:
                sources.append(f.source_url)

        # Özet oluştur
        if facts:
            summary = f"{detected_party} hakkında {len(facts)} bilgi bulundu."
        else:
            # Bilinen bilgiyi kullan
            known = self.get_known_leader(detected_party)
            if known:
                facts.append(ExtractedInfo(
                    fact=f"{detected_party} {known['title']}: {known['leader']}",
                    source_title="Güncel Bilgi",
                    source_url="",
                    confidence=1.0,
                ))
                summary = f"{detected_party} güncel bilgisi eklendi."
            else:
                summary = f"{detected_party} hakkında web'de bilgi bulunamadı."

        return SynthesizedContext(
            summary=summary,
            extracted_facts=facts,
            sources=sources,
            party=detected_party,
            query_type="person_info" if "kimdir" in query.lower() else "general",
        )


# Singleton
_synthesizer = None

def get_search_synthesizer() -> SearchSynthesizerAgent:
    global _synthesizer
    if _synthesizer is None:
        _synthesizer = SearchSynthesizerAgent()
    return _synthesizer
