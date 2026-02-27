"""
Rate Limiting Middleware
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
from typing import Dict
import logging

from ..config import settings

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Tier-based rate limiting middleware.
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.requests: Dict[str, list] = {}
    
    async def dispatch(self, request: Request, call_next):
        client_id = request.client.host if request.client else "unknown"
        
        if request.url.path.startswith("/auth/login") or request.url.path == "/":
            return await call_next(request)
        
        now = datetime.now()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < timedelta(minutes=1)
        ]
        
        if len(self.requests[client_id]) >= settings.RATE_LIMIT_PER_MINUTE:
            logger.warning(f"Rate limit exceeded for {client_id}")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        
        self.requests[client_id].append(now)
        
        response = await call_next(request)
        
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_PER_MINUTE)
        response.headers["X-RateLimit-Remaining"] = str(
            settings.RATE_LIMIT_PER_MINUTE - len(self.requests[client_id])
        )
        
        return response
