"""
Benchmark Runner
Run benchmark tests on the RAG system
"""

import asyncio
import time
import json
import logging
from typing import List, Dict, Any
from datetime import datetime

from .dataset import get_benchmark_questions, get_question_by_id
from .metrics import BenchmarkMetrics, benchmark_metrics

logger = logging.getLogger(__name__)


class BenchmarkRunner:
    """
    Benchmark runner for evaluating the RAG system.
    """
    
    def __init__(self):
        self.metrics = BenchmarkMetrics()
        self.results = []
    
    async def run_single_query(self, question: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single benchmark query.
        
        Args:
            question: Question from benchmark dataset
            
        Returns:
            Result dictionary with metrics
        """
        start_time = time.time()
        
        try:
            from src.core.cache import get_vectorstore
            from src.core.llm_setup import create_llm_handler
            
            vectorstore = get_vectorstore()
            llm, _ = create_llm_handler(question.get("party", "CHP"))
            
            docs = vectorstore.similarity_search(
                question["question"],
                k=5,
                filter={"party": question.get("party", "").upper()} if question.get("party") else None
            )
            
            context = "\n\n".join([doc.page_content for doc in docs])
            
            prompt = f"""Soru: {question['question']}

Bilgi:
{context}

Türkçe yanıt ver:"""
            
            response = llm.invoke(prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            
            latency_ms = (time.time() - start_time) * 1000
            
            retrieved_ids = [doc.metadata.get("id", "") for doc in docs]
            expected_sources = question.get("expected_sources", [])
            
            retrieval_metrics = self.metrics.evaluate_retrieval(
                retrieved_ids, expected_sources
            )
            
            generation_metrics = self.metrics.evaluate_generation(
                answer,
                question.get("ground_truth_keywords", []),
                context
            )
            
            result = {
                "question_id": question["id"],
                "question": question["question"],
                "answer": answer,
                "retrieved_docs": retrieved_ids,
                "latency_ms": latency_ms,
                "success": True,
                "retrieval_metrics": retrieval_metrics,
                "generation_metrics": generation_metrics,
            }
            
        except Exception as e:
            logger.error(f"Error running query {question['id']}: {e}")
            result = {
                "question_id": question["id"],
                "question": question["question"],
                "error": str(e),
                "success": False,
                "latency_ms": (time.time() - start_time) * 1000,
            }
        
        self.results.append(result)
        return result
    
    async def run_all(self, max_questions: int = None) -> List[Dict[str, Any]]:
        """
        Run all benchmark questions.
        
        Args:
            max_questions: Maximum number of questions to run
            
        Returns:
            List of results
        """
        questions = get_benchmark_questions()
        
        if max_questions:
            questions = questions[:max_questions]
        
        logger.info(f"Running {len(questions)} benchmark questions...")
        
        for i, question in enumerate(questions, 1):
            logger.info(f"Running question {i}/{len(questions)}: {question['id']}")
            await self.run_single_query(question)
        
        return self.results
    
    def get_summary(self) -> Dict[str, Any]:
        """Get benchmark summary."""
        if not self.results:
            return {}
        
        successful = [r for r in self.results if r.get("success", False)]
        
        avg_latency = sum(r.get("latency_ms", 0) for r in successful) / len(successful) if successful else 0
        
        retrieval_metrics = {}
        generation_metrics = {}
        
        for r in successful:
            for k, v in r.get("retrieval_metrics", {}).items():
                if k not in retrieval_metrics:
                    retrieval_metrics[k] = []
                retrieval_metrics[k].append(v)
            
            for k, v in r.get("generation_metrics", {}).items():
                if k not in generation_metrics:
                    generation_metrics[k] = []
                generation_metrics[k].append(v)
        
        summary = {
            "total_questions": len(self.results),
            "successful": len(successful),
            "failed": len(self.results) - len(successful),
            "success_rate": len(successful) / len(self.results) if self.results else 0,
            "avg_latency_ms": avg_latency,
            "retrieval": {
                k: sum(v) / len(v) if v else 0
                for k, v in retrieval_metrics.items()
            },
            "generation": {
                k: sum(v) / len(v) if v else 0
                for k, v in generation_metrics.items()
            },
            "timestamp": datetime.now().isoformat(),
        }
        
        return summary
    
    def export_results(self, filepath: str):
        """Export results to JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "results": self.results,
                "summary": self.get_summary()
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Results exported to {filepath}")


async def run_benchmark(max_questions: int = None) -> Dict[str, Any]:
    """
    Convenience function to run benchmark.
    
    Args:
        max_questions: Maximum questions to run
        
    Returns:
        Benchmark summary
    """
    runner = BenchmarkRunner()
    await runner.run_all(max_questions)
    return runner.get_summary()
