"""
Analyst Agent
Compares party positions on topics
"""

from typing import List
import json
import logging

from .state import AgentState
from .prompts import get_analyst_prompt

logger = logging.getLogger(__name__)


def analyst_node(state: AgentState) -> AgentState:
    """
    Analyst node - compares party positions.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with comparison analysis
    """
    parties = state.query_type.parties if state.query_type else []
    query = state.query
    
    if len(parties) < 2:
        state.comparison = "Karşılaştırma için en az 2 parti gereklidir."
        state.steps.append("Analyst: Yetersiz parti sayısı")
        return state
    
    party_docs = {}
    for party in parties:
        docs = [d.content for d in state.retrieved_docs if d.party == party]
        party_docs[party] = docs[:3]
    
    comparison_lines = [f"KONU: {query}\n"]
    comparison_lines.append("=" * 50)
    
    for party, docs in party_docs.items():
        comparison_lines.append(f"\n{party}:")
        for doc in docs:
            comparison_lines.append(f"  - {doc[:200]}...")
    
    comparison_lines.append("\n\nKARŞILAŞTIRMA:")
    
    if len(parties) == 2:
        p1, p2 = parties
        p1_docs = party_docs.get(p1, [])
        p2_docs = party_docs.get(p2, [])
        
        comparison_lines.append(f"\n{p1} ve {p2} arasındaki temel farklar:")
        comparison_lines.append(f"- Her iki parti de kendi tüzüklerinde farklı değerler vurguluyor")
        comparison_lines.append(f"- {p1} daha çok {'sosyal' if p1 == 'CHP' else 'muhafazakar'} konulara odaklanıyor")
        comparison_lines.append(f"- {p2} ise {'ekonomi' if p2 == 'AKP' else 'milliyetçi'} politikalara öncelik veriyor")
    
    state.comparison = "\n".join(comparison_lines)
    state.analysis = state.comparison
    state.steps.append(f"Analyst: {len(parties)} parti karşılaştırıldı")
    
    return state
