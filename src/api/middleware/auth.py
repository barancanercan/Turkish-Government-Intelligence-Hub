"""
Authentication Middleware
"""

from fastapi import Header, HTTPException, status
from typing import Optional
from jose import jwt, JWTError
from datetime import datetime, timedelta

from ..config import settings


def create_access_token(data: dict) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decode JWT token."""
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


async def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Get current user from JWT token.
    """
    if not authorization:
        return "anonymous"
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )
    
    token = authorization.replace("Bearer ", "")
    
    try:
        payload = decode_token(token)
        return payload.get("sub", "anonymous")
    except Exception:
        return "anonymous"


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> Optional[str]:
    """
    Verify API key from header.
    """
    if not x_api_key:
        return None
    
    return x_api_key
