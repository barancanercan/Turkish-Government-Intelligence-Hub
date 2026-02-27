"""
Benchmark Package
Gold dataset, metrics, and runner
"""

from .dataset import GOLD_DATASET, get_benchmark_questions, get_question_by_id
from .metrics import (
    BenchmarkMetrics,
    benchmark_metrics,
    calculate_recall_at_k,
    calculate_precision_at_k,
    calculate_mrr,
    calculate_ndcg,
)
from .runner import BenchmarkRunner, run_benchmark

__all__ = [
    "GOLD_DATASET",
    "get_benchmark_questions",
    "get_question_by_id",
    "BenchmarkMetrics",
    "benchmark_metrics",
    "calculate_recall_at_k",
    "calculate_precision_at_k",
    "calculate_mrr",
    "calculate_ndcg",
    "BenchmarkRunner",
    "run_benchmark",
]
