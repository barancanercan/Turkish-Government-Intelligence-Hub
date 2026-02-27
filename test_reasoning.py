#!/usr/bin/env python3
"""
Test script for Chain-of-Thought Reasoning Module
"""

from src.core.reasoning import ReasoningEngine, enhance_query_with_reasoning


def test_question_analysis():
    """Test soru analiz fonksiyonu."""
    test_questions = [
        "CHP kimdedir?",
        "AKP nedir?",
        "Nasil secim yapilir?",
        "Neden MHP ile AKP birlikte calisiyorlar?",
        "CHP ve AKP arasindaki fark nedir?",
    ]

    print("=" * 60)
    print("SORU ANALIZ TESTLERI")
    print("=" * 60)

    for question in test_questions:
        analysis = ReasoningEngine.analyze_question(question)
        print(f"\nSoru: {question}")
        print(f"  Tip: {analysis['type']}")
        print(f"  Partiler: {analysis['parties']}")
        print(f"  Karsilastirma Gerekli: {analysis['requires_comparison']}")


def test_cot_prompt():
    """Test Chain-of-Thought prompt olusturma."""
    question = "AKP'nin temel ilkeleri nedir?"
    context = "AKP, 2001 yilinda kurulmus ve muhafazakar ideolojiyi temsil etmektedir. Temel ilkeleri: 1. Adalet, 2. Kalkinma, 3. Kalkınma"

    print("\n" + "=" * 60)
    print("CHAIN-OF-THOUGHT PROMPT TESTI")
    print("=" * 60)

    analysis = ReasoningEngine.analyze_question(question)
    cot_prompt = ReasoningEngine.build_cot_prompt(question, context, analysis)

    print(f"\nOlusturulan Prompt:\n")
    print(cot_prompt)


def test_enhance_query():
    """Test query zenginlestirme fonksiyonu."""
    question = "CHP ve MHP'nin politikalari arasinda ne fark var?"
    context = "CHP sosyal demokrasi, MHP milliyetcilik iletiyor..."

    print("\n" + "=" * 60)
    print("QUERY ZENGINLESTIRME TESTI")
    print("=" * 60)

    enhanced_prompt, analysis = enhance_query_with_reasoning(question, context)

    print(f"\nOrijinal Soru: {question}")
    print(f"Analiz Sonucu:")
    print(f"  - Soru Tipi: {analysis['type']}")
    print(f"  - Ilgili Partiler: {analysis['parties']}")
    print(f"  - Karsilastirma Gerekli: {analysis['requires_comparison']}")
    print(f"\nZenginlestirilmis Prompt:\n")
    print(enhanced_prompt[:300] + "...\n")


if __name__ == "__main__":
    test_question_analysis()
    test_cot_prompt()
    test_enhance_query()
    print("\n" + "=" * 60)
    print("TUM TESTLER TAMAMLANDI")
    print("=" * 60)
