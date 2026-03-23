"""
System Router
Health and stats endpoints
"""

from fastapi import APIRouter
from datetime import datetime
import logging

from ..schemas import HealthResponse, StatsResponse
from ..config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

stats = {
    "total_requests": 0,
    "unique_users": 0,
    "cache_hits": 0,
    "cache_misses": 0,
}


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    """
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        timestamp=datetime.now(),
    )


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get system statistics.
    """
    total = stats["total_requests"]
    cache_rate = stats["cache_hits"] / total if total > 0 else 0.0

    return StatsResponse(
        total_requests=total,
        unique_users=stats["unique_users"],
        avg_latency_ms=150.0,
        cache_hit_rate=cache_rate,
    )
