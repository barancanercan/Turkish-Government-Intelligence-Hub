"""
Pydantic Schemas for Request/Response Models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class QueryRequest(BaseModel):
    """Query request schema."""
    question: str = Field(..., min_length=1, max_length=500, description="User question")
    party: Optional[str] = Field(None, description="Optional party filter")
    top_k: int = Field(5, ge=1, le=20, description="Number of results")
    stream: bool = Field(False, description="Enable streaming response")


class QueryResponse(BaseModel):
    """Query response schema."""
    answer: str
    sources: List[str] = []
    citations: List[str] = []
    query_type: str = "simple"
    latency_ms: float = 0.0


class CompareRequest(BaseModel):
    """Compare request schema."""
    question: str = Field(..., description="Comparison question")
    parties: List[str] = Field(..., min_items=2, max_items=8, description="Parties to compare")
    top_k: int = Field(5, ge=1, le=20)


class CompareResponse(BaseModel):
    """Compare response schema."""
    comparison: str
    party_positions: Dict[str, str] = {}
    sources: List[str] = []
    latency_ms: float = 0.0


class AnalyzeRequest(BaseModel):
    """Deep analysis request schema."""
    question: str = Field(..., description="Analysis question")
    parties: List[str] = Field(default_factory=list)
    include_web: bool = Field(True, description="Include web search")


class AnalyzeResponse(BaseModel):
    """Analysis response schema."""
    analysis: str
    key_findings: List[str] = []
    sources: List[str] = []
    web_results: List[Dict[str, str]] = []
    latency_ms: float = 0.0


class PartyInfo(BaseModel):
    """Party information schema."""
    code: str
    name: str
    short_name: str
    website: Optional[str] = None
    hex_color: Optional[str] = None
    ideology: Optional[str] = None
    founded: Optional[int] = None
    description: Optional[str] = None


class PartyListResponse(BaseModel):
    """Party list response."""
    parties: List[PartyInfo]
    total: int


class TokenRequest(BaseModel):
    """Token request schema."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserCreate(BaseModel):
    """User creation schema."""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    """User response schema."""
    id: str
    username: str
    email: str
    tier: str = "free"
    created_at: datetime


class UsageResponse(BaseModel):
    """Usage statistics response."""
    requests_today: int
    requests_remaining: int
    tier: str
    reset_at: datetime


class FeedbackRequest(BaseModel):
    """Feedback request schema."""
    query_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    """Feedback response schema."""
    success: bool
    message: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime


class StatsResponse(BaseModel):
    """System statistics response."""
    total_requests: int
    unique_users: int
    avg_latency_ms: float
    cache_hit_rate: float
