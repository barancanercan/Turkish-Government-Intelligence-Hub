"""
Gold QA Dataset
Benchmark questions with ground truth
"""

from typing import List, Dict, Any


GOLD_DATASET = {
    "version": "1.0",
    "questions": [
        {
            "id": "q001",
            "question": "CHP'nin laiklik ilkesine yaklaşımı nedir?",
            "difficulty": "easy",
            "type": "single_party",
            "expected_sources": ["chp_tuzuk.pdf"],
            "ground_truth_keywords": ["laiklik", "cumhuriyet", "devrim", "ataturk"],
            "party": "CHP"
        },
        {
            "id": "q002",
            "question": "AKP ve MHP'nin dış politika yaklaşımları nasıl farklılaşır?",
            "difficulty": "hard",
            "type": "comparison",
            "expected_sources": ["akp_tuzuk.pdf", "mhp_tuzuk.pdf"],
            "ground_truth_keywords": ["AB", "NATO", "Turkiye", "dis politika"],
            "parties": ["AKP", "MHP"]
        },
        {
            "id": "q003",
            "question": "İYİ Parti'nin ekonomi politikası neyi savunur?",
            "difficulty": "medium",
            "type": "single_party",
            "expected_sources": ["iyi_tuzuk.pdf"],
            "ground_truth_keywords": ["piyasa", "dengel", "ekonomi", "istikrar"],
            "party": "İYİ"
        },
        {
            "id": "q004",
            "question": "Demokrat Parti'nin sosyal politika anlayışı nedir?",
            "difficulty": "medium",
            "type": "single_party",
            "expected_sources": ["dem_tuzuk.pdf"],
            "ground_truth_keywords": ["sosyal", "adalet", "esitlik", "toplum"],
            "party": "DEM"
        },
        {
            "id": "q005",
            "question": "AKP'nin eğitim politikasının temel ilkeleri nelerdir?",
            "difficulty": "easy",
            "type": "single_party",
            "expected_sources": ["akp_tuzuk.pdf"],
            "ground_truth_keywords": ["egitim", "ogrenci", "ogretmen", "okul"],
            "party": "AKP"
        },
        {
            "id": "q006",
            "question": "MHP'nin ulusal güvenlik politikası nedir?",
            "difficulty": "medium",
            "type": "single_party",
            "expected_sources": ["mhp_tuzuk.pdf"],
            "ground_truth_keywords": ["guvenlik", "savunma", "teror", "sinir"],
            "party": "MHP"
        },
        {
            "id": "q007",
            "question": "CHP ve İYİ Parti'nin çevre politikaları karşılaştırıldığında ne gibi farklar var?",
            "difficulty": "hard",
            "type": "comparison",
            "expected_sources": ["chp_tuzuk.pdf", "iyi_tuzuk.pdf"],
            "ground_truth_keywords": ["cevre", "iklim", "yeşil", "dogal"],
            "parties": ["CHP", "İYİ"]
        },
        {
            "id": "q008",
            "question": "Saadet Partisi'nin adalet anlayışı ne üzerine kuruludur?",
            "difficulty": "medium",
            "type": "single_party",
            "expected_sources": ["sp_tuzuk.pdf"],
            "ground_truth_keywords": ["adalet", "hukuk", "doganin", "haklar"],
            "party": "SP"
        },
        {
            "id": "q009",
            "question": "Zafer Partisi'nin AB'ye yaklaşımı nedir?",
            "difficulty": "medium",
            "type": "single_party",
            "expected_sources": ["zp_tuzuk.pdf"],
            "ground_truth_keywords": ["AB", "Avrupa", "uyum", "mukur"],
            "party": "ZP"
        },
        {
            "id": "q010",
            "question": "BBP'nin milliyetçilik anlayışı nasıl tanımlanır?",
            "difficulty": "easy",
            "type": "single_party",
            "expected_sources": ["bbp_tuzuk.pdf"],
            "ground_truth_keywords": ["milliyet", "turk", "birlik", "devlet"],
            "party": "BBP"
        }
    ]
}


def get_benchmark_questions() -> List[Dict[str, Any]]:
    """Get all benchmark questions."""
    return GOLD_DATASET["questions"]


def get_question_by_id(qid: str) -> Dict[str, Any]:
    """Get question by ID."""
    for q in GOLD_DATASET["questions"]:
        if q["id"] == qid:
            return q
    return None


def get_questions_by_difficulty(difficulty: str) -> List[Dict[str, Any]]:
    """Get questions by difficulty level."""
    return [q for q in GOLD_DATASET["questions"] if q["difficulty"] == difficulty]


def get_questions_by_type(qtype: str) -> List[Dict[str, Any]]:
    """Get questions by type."""
    return [q for q in GOLD_DATASET["questions"] if q["type"] == qtype]
