"""
Benchmark Metrics
Retrieval, Generation, and System metrics
"""

from typing import List, Dict, Any, Set
import logging

logger = logging.getLogger(__name__)


def calculate_recall_at_k(retrieved: List[str], relevant: List[str], k: int = 5) -> float:
    """
    Calculate Recall@K metric.
    
    Args:
        retrieved: List of retrieved document IDs
        relevant: List of relevant document IDs
        k: Number of top results to consider
        
    Returns:
        Recall@K score
    """
    if not relevant:
        return 0.0
    
    retrieved_k = set(retrieved[:k])
    relevant_set = set(relevant)
    
    intersection = retrieved_k.intersection(relevant_set)
    
    return len(intersection) / len(relevant_set)


def calculate_precision_at_k(retrieved: List[str], relevant: List[str], k: int = 5) -> float:
    """
    Calculate Precision@K metric.
    
    Args:
        retrieved: List of retrieved document IDs
        relevant: List of relevant document IDs
        k: Number of top results to consider
        
    Returns:
        Precision@K score
    """
    retrieved_k = set(retrieved[:k])
    
    if not retrieved_k:
        return 0.0
    
    relevant_set = set(relevant)
    intersection = retrieved_k.intersection(relevant_set)
    
    return len(intersection) / k


def calculate_mrr(retrieved: List[str], relevant: List[str]) -> float:
    """
    Calculate Mean Reciprocal Rank (MRR).
    
    Args:
        retrieved: List of retrieved document IDs
        relevant: List of relevant document IDs
        
    Returns:
        MRR score
    """
    relevant_set = set(relevant)
    
    for i, doc_id in enumerate(retrieved, 1):
        if doc_id in relevant_set:
            return 1.0 / i
    
    return 0.0


def calculate_ndcg(retrieved: List[str], relevant: List[str], k: int = 5) -> float:
    """
    Calculate Normalized Discounted Cumulative Gain (NDCG).
    
    Args:
        retrieved: List of retrieved document IDs
        relevant: List of relevant document IDs
        k: Number of top results to consider
        
    Returns:
        NDCG score
    """
    relevant_set = set(relevant)
    
    dcg = 0.0
    for i, doc_id in enumerate(retrieved[:k], 1):
        if doc_id in relevant_set:
            dcg += 1.0 / (i if i <= 10 else 1)
    
    idcg = sum(1.0 / (i if i <= 10 else 1) for i in range(1, min(k, len(relevant_set)) + 1))
    
    if idcg == 0:
        return 0.0
    
    return dcg / idcg


def calculate_keyword_overlap(answer: str, keywords: List[str]) -> float:
    """
    Calculate keyword overlap for generation quality.
    
    Args:
        answer: Generated answer
        keywords: Ground truth keywords
        
    Returns:
        Keyword overlap score
    """
    answer_lower = answer.lower()
    
    matched = sum(1 for kw in keywords if kw.lower() in answer_lower)
    
    return matched / len(keywords) if keywords else 0.0


def calculate_faithfulness(context: str, answer: str) -> float:
    """
    Calculate faithfulness score based on context.
    
    Args:
        context: Source context
        answer: Generated answer
        
    Returns:
        Faithfulness score
    """
    context_lower = context.lower()
    answer_lower = answer.lower()
    
    context_words = set(context_lower.split())
    answer_words = set(answer_lower.split())
    
    if not answer_words:
        return 0.0
    
    overlap = answer_words.intersection(context_words)
    
    return len(overlap) / len(answer_words)


class BenchmarkMetrics:
    """
    Comprehensive benchmark metrics calculator.
    """
    
    def __init__(self):
        self.results = []
    
    def evaluate_retrieval(
        self,
        retrieved_docs: List[str],
        expected_sources: List[str],
        k_values: List[int] = [1, 3, 5, 10]
    ) -> Dict[str, float]:
        """Evaluate retrieval quality."""
        metrics = {}
        
        for k in k_values:
            metrics[f"recall@{k}"] = calculate_recall_at_k(retrieved_docs, expected_sources, k)
            metrics[f"precision@{k}"] = calculate_precision_at_k(retrieved_docs, expected_sources, k)
        
        metrics["mrr"] = calculate_mrr(retrieved_docs, expected_sources)
        metrics["ndcg@5"] = calculate_ndcg(retrieved_docs, expected_sources, 5)
        
        return metrics
    
    def evaluate_generation(
        self,
        answer: str,
        ground_truth_keywords: List[str],
        context: str = ""
    ) -> Dict[str, float]:
        """Evaluate generation quality."""
        metrics = {}
        
        metrics["keyword_overlap"] = calculate_keyword_overlap(answer, ground_truth_keywords)
        
        if context:
            metrics["faithfulness"] = calculate_faithfulness(context, answer)
        
        metrics["answer_length"] = len(answer.split())
        
        return metrics
    
    def evaluate_system(
        self,
        latency_ms: float,
        success: bool = True
    ) -> Dict[str, float]:
        """Evaluate system performance."""
        return {
            "latency_ms": latency_ms,
            "success": 1.0 if success else 0.0,
        }
    
    def add_result(self, result: Dict[str, Any]):
        """Add a benchmark result."""
        self.results.append(result)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all results."""
        if not self.results:
            return {}
        
        summary = {
            "total_questions": len(self.results),
            "successful": sum(1 for r in self.results if r.get("success", False)),
            "avg_latency_ms": sum(r.get("latency_ms", 0) for r in self.results) / len(self.results),
        }
        
        return summary


benchmark_metrics = BenchmarkMetrics()
