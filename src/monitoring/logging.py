"""
Structured Logging
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
import uuid


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


class RequestLogger:
    """
    Request logger with request ID tracking.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("mizan-requests")
        self.request_logs = {}
    
    def start_request(self, request_id: Optional[str] = None) -> str:
        """Start tracking a request."""
        if not request_id:
            request_id = str(uuid.uuid4())
        
        self.request_logs[request_id] = {
            "id": request_id,
            "start_time": datetime.now(),
            "steps": [],
        }
        
        return request_id
    
    def log_step(self, request_id: str, step: str, data: Optional[Dict[str, Any]] = None):
        """Log a request step."""
        if request_id not in self.request_logs:
            return
        
        self.request_logs[request_id]["steps"].append({
            "step": step,
            "timestamp": datetime.now().isoformat(),
            "data": data or {},
        })
    
    def end_request(self, request_id: str, status: str = "success", error: Optional[str] = None):
        """End tracking a request."""
        if request_id not in self.request_logs:
            return
        
        log_entry = self.request_logs[request_id]
        log_entry["end_time"] = datetime.now().isoformat()
        log_entry["status"] = status
        log_entry["duration_ms"] = (
            datetime.now() - log_entry["start_time"]
        ).total_seconds() * 1000
        
        if error:
            log_entry["error"] = error
        
        self.logger.info(f"Request {request_id}: {status}", extra={
            "request_id": request_id,
            "log": log_entry,
        })
        
        del self.request_logs[request_id]
        
        return log_entry
    
    def get_request_log(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get log for a specific request."""
        return self.request_logs.get(request_id)


request_logger = RequestLogger()


def setup_logging(log_level: str = "INFO"):
    """
    Setup structured logging.
    
    Args:
        log_level: Logging level
    """
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JSONFormatter())
    
    logger.addHandler(console_handler)
    
    file_handler = logging.FileHandler("mizan-ai.log")
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)
    
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
