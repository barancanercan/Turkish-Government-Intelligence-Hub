"""
Auth Router
Authentication endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
import logging

from ..schemas import TokenRequest, TokenResponse, UserCreate, UserResponse, UsageResponse
from ..config import settings
from ..middleware.auth import create_access_token

router = APIRouter()
logger = logging.getLogger(__name__)

users_db = {}


@router.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    """
    Register a new user.
    """
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    users_db[user.username] = {
        "id": f"user_{len(users_db) + 1}",
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "tier": "free",
        "created_at": datetime.now(),
    }

    return UserResponse(
        id=users_db[user.username]["id"],
        username=user.username,
        email=user.email,
        tier="free",
        created_at=users_db[user.username]["created_at"],
    )


@router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: TokenRequest):
    """
    Login and get access token.
    """
    user = users_db.get(credentials.username)

    if not user or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user["username"], "tier": user["tier"]}
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.get("/usage", response_model=UsageResponse)
async def get_usage(user_id: str = Depends(lambda: "demo_user")):
    """
    Get usage statistics for current user.
    """
    return UsageResponse(
        requests_today=5,
        requests_remaining=settings.FREE_TIER_DAILY - 5,
        tier="free",
        reset_at=datetime.now() + timedelta(days=1),
    )


@router.post("/feedback", response_model=dict)
async def submit_feedback(
    query_id: str,
    rating: int,
    comment: str = None,
    user_id: str = Depends(lambda: "demo_user"),
):
    """
    Submit feedback for a query.
    """
    logger.info(f"Feedback: query={query_id}, rating={rating}, user={user_id}")

    return {"success": True, "message": "Feedback received"}
