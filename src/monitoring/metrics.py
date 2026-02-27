"""
Prometheus Metrics Exporter
"""

import time
from typing import Dict, Any, Optional
from collections import defaultdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Custom metrics collector for the application.
    """
    
    def __init__(self):
        self.counters = defaultdict(int)
        self.gauges = {}
        self.histograms = defaultdict(list)
        self.timers = {}
        
        self.query_counts = defaultdict(int)
        self.query_latencies = defaultdict(list)
        self.party_queries = defaultdict(int)
        self.error_counts = defaultdict(int)
        
        self.start_time = time.time()
    
    def increment_counter(self, name: str, value: int = 1, labels: Optional[Dict[str, str]] = None):
        """Increment a counter metric."""
        key = self._make_key(name, labels)
        self.counters[key] += value
    
    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Set a gauge metric."""
        key = self._make_key(name, labels)
        self.gauges[key] = value
    
    def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Observe a histogram value."""
        key = self._make_key(name, labels)
        self.histograms[key].append(value)
    
    def start_timer(self, name: str) -> float:
        """Start a timer."""
        self.timers[name] = time.time()
        return self.timers[name]
    
    def stop_timer(self, name: str) -> Optional[float]:
        """Stop a timer and return elapsed time."""
        if name not in self.timers:
            return None
        
        elapsed = time.time() - self.timers[name]
        del self.timers[name]
        
        self.observe_histogram(f"{name}_seconds", elapsed)
        return elapsed
    
    def _make_key(self, name: str, labels: Optional[Dict[str, str]] = None) -> str:
        """Create a metric key with labels."""
        if not labels:
            return name
        
        label_str = ",".join(f'{k}="{v}"' for k, v in labels.items())
        return f"{name}{{{label_str}}}"
    
    def record_query(self, query_type: str, latency_ms: float, party: Optional[str] = None, success: bool = True):
        """Record a query execution."""
        self.query_counts[query_type] += 1
        self.query_latencies[query_type].append(latency_ms)
        
        if party:
            self.party_queries[party] += 1
        
        if not success:
            self.error_counts[query_type] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        uptime = time.time() - self.start_time
        
        return {
            "uptime_seconds": uptime,
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "queries": {
                "by_type": dict(self.query_counts),
                "by_party": dict(self.party_queries),
                "errors": dict(self.error_counts),
                "latencies": {
                    k: {
                        "count": len(v),
                        "mean": sum(v) / len(v) if v else 0,
                        "p50": self._percentile(v, 0.5),
                        "p95": self._percentile(v, 0.95),
                        "p99": self._percentile(v, 0.99),
                    }
                    for k, v in self.query_latencies.items()
                },
            },
        }
    
    def _percentile(self, values: list, p: float) -> float:
        """Calculate percentile."""
        if not values:
            return 0.0
        sorted_values = sorted(values)
        idx = int(len(sorted_values) * p)
        return sorted_values[min(idx, len(sorted_values) - 1)]
    
    def reset(self):
        """Reset all metrics."""
        self.counters.clear()
        self.gauges.clear()
        self.histograms.clear()
        self.timers.clear()
        self.query_counts.clear()
        self.query_latencies.clear()
        self.party_queries.clear()
        self.error_counts.clear()


metrics_collector = MetricsCollector()


def get_prometheus_metrics() -> str:
    """
    Get metrics in Prometheus format.
    
    Returns:
        Prometheus-formatted metrics string
    """
    metrics = metrics_collector.get_metrics()
    lines = []
    
    lines.append(f'# HELP mizan_uptime_seconds Application uptime in seconds')
    lines.append(f'# TYPE mizan_uptime_seconds gauge')
    lines.append(f'mizan_uptime_seconds {metrics["uptime_seconds"]}')
    
    for name, value in metrics["counters"].items():
        lines.append(f'# HELP {name} Counter metric')
        lines.append(f'# TYPE {name} counter')
        lines.append(f'{name} {value}')
    
    for name, value in metrics["gauges"].items():
        lines.append(f'# HELP {name} Gauge metric')
        lines.append(f'# TYPE {name} gauge')
        lines.append(f'{name} {value}')
    
    for qtype, latencies in metrics["queries"]["latencies"].items():
        safe_name = qtype.replace("-", "_")
        lines.append(f'# HELP query_latency_seconds Query latency')
        lines.append(f'# TYPE query_latency_seconds summary')
        lines.append(f'query_latency_seconds_count{{type="{qtype}"}} {latencies["count"]}')
        lines.append(f'query_latency_seconds_sum{{type="{qtype}"}} {latencies["mean"] * latencies["count"]}')
    
    return "\n".join(lines)
