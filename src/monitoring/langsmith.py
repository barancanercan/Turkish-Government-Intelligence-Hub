"""
LangSmith Integration
Trace instrumentation and monitoring
"""

import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

langsmith_available = False

try:
    from langsmith import Client
    from langchain_core.callbacks import LangChainCallbackHandler
    langsmith_available = True
except ImportError:
    logger.warning("LangSmith not installed")


class LangSmithTracer:
    """
    LangSmith tracer for agent traces.
    """
    
    def __init__(self, project_name: str = "mizan-ai"):
        self.project_name = project_name
        self.client = None
        self.tracer = None
        
        api_key = os.environ.get("LANGSMITH_API_KEY")
        if api_key and langsmith_available:
            try:
                self.client = Client(api_key=api_key)
                self.tracer = LangChainCallbackHandler(
                    project_name=project_name,
                    client=self.client,
                )
                logger.info(f"LangSmith tracer initialized: {project_name}")
            except Exception as e:
                logger.warning(f"LangSmith init failed: {e}")
    
    def get_callback_handler(self):
        """Get callback handler for LangChain."""
        return self.tracer
    
    def log_run(self, run_data: Dict[str, Any]):
        """Log a custom run to LangSmith."""
        if not self.client:
            return
        
        try:
            self.client.create_run(
                project_name=self.project_name,
                run_type="chain",
                name=run_data.get("name", "unknown"),
                inputs=run_data.get("inputs", {}),
                outputs=run_data.get("outputs", {}),
                start_time=run_data.get("start_time", datetime.now()),
                end_time=run_data.get("end_time", datetime.now()),
            )
        except Exception as e:
            logger.error(f"LangSmith log error: {e}")


def create_tracer(project_name: str = "mizan-ai") -> Optional[LangSmithTracer]:
    """
    Create a LangSmith tracer.
    
    Args:
        project_name: Project name for traces
        
    Returns:
        LangSmithTracer instance or None
    """
    return LangSmithTracer(project_name)


class CostTracker:
    """
    Track LLM costs and usage.
    """
    
    def __init__(self):
        self.total_cost = 0.0
        self.total_tokens = 0
        self.total_requests = 0
        self.model_costs = {
            "gemini-2.0-flash": {"input": 0.0, "output": 0.0},
            "qwen2.5:7b": {"input": 0.0, "output": 0.0},
        }
    
    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost for a request.
        
        Args:
            model: Model name
            input_tokens: Input token count
            output_tokens: Output token count
            
        Returns:
            Cost in USD
        """
        input_cost_per_1k = 0.0
        output_cost_per_1k = 0.0
        
        if "gemini" in model.lower():
            input_cost_per_1k = 0.000035
            output_cost_per_1k = 0.00014
        elif "qwen" in model.lower():
            input_cost_per_1k = 0.0001
            output_cost_per_1k = 0.0001
        
        cost = (input_tokens / 1000 * input_cost_per_1k) + (output_tokens / 1000 * output_cost_per_1k)
        
        self.total_cost += cost
        self.total_tokens += input_tokens + output_tokens
        self.total_requests += 1
        
        return cost
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cost statistics."""
        return {
            "total_cost": self.total_cost,
            "total_tokens": self.total_tokens,
            "total_requests": self.total_requests,
            "avg_cost_per_request": self.total_cost / max(self.total_requests, 1),
            "avg_tokens_per_request": self.total_tokens / max(self.total_requests, 1),
        }
    
    def reset(self):
        """Reset counters."""
        self.total_cost = 0.0
        self.total_tokens = 0
        self.total_requests = 0


cost_tracker = CostTracker()
