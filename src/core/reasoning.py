"""
Chain-of-Thought Reasoning Module
Provides question analysis and step-by-step reasoning capabilities.
"""

from typing import Dict, Any, Tuple
import re


class ReasoningEngine:
    """Soru analizi ve adim adim dusunme motoru."""

    QUESTION_TYPES = {
        "kimdir": "PERSON_INFO",
        "nedir": "DEFINITION",
        "nasil": "PROCESS",
        "neden": "REASON",
        "ne zaman": "TIME",
        "kac": "QUANTITY",
        "karsilastir": "COMPARISON",
        "farki": "COMPARISON",
    }

    @classmethod
    def analyze_question(cls, question: str) -> Dict[str, Any]:
        """Soruyu analiz et ve tipini belirle."""
        question_lower = question.lower()

        # Tum eslesen tipleri bul (coklu soru desteği)
        detected_types = []
        for keyword, qtype in cls.QUESTION_TYPES.items():
            if keyword in question_lower:
                detected_types.append(qtype)

        if not detected_types:
            detected_types = ["GENERAL"]

        # Ana tip ilk bulunan
        detected_type = detected_types[0]

        # Parti tespiti
        parties = []
        party_keywords = ["chp", "akp", "mhp", "iyi", "dem", "sp", "zp", "bbp"]
        for party in party_keywords:
            if party in question_lower:
                parties.append(party.upper())

        # Soru parcalari (ve/veya ile ayrilmis)
        sub_questions = []
        if " ve " in question_lower or " nasil " in question_lower:
            # "kimdir ve nasil secilir" gibi sorulari parcala
            if "kimdir" in question_lower:
                sub_questions.append("Kisi kim? (isim ver)")
            if "nasil" in question_lower:
                sub_questions.append("Surec nasil isliyor? (adimlari acikla)")
            if "nedir" in question_lower:
                sub_questions.append("Tanim nedir?")

        return {
            "original": question,
            "type": detected_type,
            "all_types": detected_types,
            "sub_questions": sub_questions,
            "parties": parties,
            "requires_comparison": detected_type == "COMPARISON" or len(parties) > 1,
            "is_compound": len(detected_types) > 1 or len(sub_questions) > 1,
        }

    @classmethod
    def build_cot_prompt(cls, question: str, context: str, analysis: Dict[str, Any]) -> str:
        """Chain-of-Thought prompt olustur."""

        type_instructions = {
            "PERSON_INFO": "Kisi bilgisi isteniyor. ISIM ver.",
            "DEFINITION": "Tanim isteniyor. Kavrami acikla.",
            "PROCESS": "Surec isteniyor. Adimlari sirala.",
            "REASON": "Sebep isteniyor. Nedenleri acikla.",
            "TIME": "Zaman bilgisi isteniyor. Tarih veya donem belirt.",
            "QUANTITY": "Sayi/miktar isteniyor. Rakam ver.",
            "COMPARISON": "Karsilastirma isteniyor. Benzerlikleri ve farklari listele.",
            "GENERAL": "Genel bilgi isteniyor. Ozet ver.",
        }

        # Coklu soru icin tum talimatlari birleştir
        if analysis.get("is_compound") and analysis.get("sub_questions"):
            instruction = "COKLU SORU - Her bir alt soruyu AYRI AYRI yanitla:\n"
            for i, sub_q in enumerate(analysis["sub_questions"], 1):
                instruction += f"  {i}. {sub_q}\n"
        else:
            instruction = type_instructions.get(analysis["type"], type_instructions["GENERAL"])

        prompt = f"""Sen Turk siyasi partileri uzmanisin.

ONEMLI KURALLAR:
1. Soruda "kimdir" varsa MUTLAKA bir ISIM ver (ornegin: "Ozgur Ozel", "Kemal Kilicdaroglu")
2. Soruda "nasil" varsa SURECI acikla
3. Soruda birden fazla soru varsa HER BIRINI ayri ayri yanitla
4. Belgede isim yoksa "Mevcut belgelerde isim bilgisi bulunmuyor" de

SORU: {question}
SORU TIPI: {analysis["type"]}
PARTI: {", ".join(analysis["parties"]) if analysis["parties"] else "Genel"}

TALIMAT: {instruction}

KAYNAK BILGI:
{context}

YANITIM (her alt soruyu ayri yanitliyorum):
"""
        return prompt


def enhance_query_with_reasoning(question: str, context: str) -> Tuple[str, Dict[str, Any]]:
    """Soruyu reasoning ile zenginlestir."""
    analysis = ReasoningEngine.analyze_question(question)
    enhanced_prompt = ReasoningEngine.build_cot_prompt(question, context, analysis)
    return enhanced_prompt, analysis
