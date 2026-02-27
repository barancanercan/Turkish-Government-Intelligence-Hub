"""
FastAPI Application Entry Point
Production-Grade API for MIZAN-AI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .config import settings
from .routers import query, parties, auth, system
from .middleware.rate_limit import RateLimitMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    logger.info("MIZAN-AI API starting up...")
    yield
    logger.info("MIZAN-AI API shutting down...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title="MIZAN-AI API",
        description="Political Document Analysis API with RAG",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(RateLimitMiddleware)
    
    app.include_router(query.router, prefix="/api/v1", tags=["Query"])
    app.include_router(parties.router, prefix="/api/v1", tags=["Parties"])
    app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
    app.include_router(system.router, prefix="/api/v1", tags=["System"])
    
    return app


app = create_app()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "MIZAN-AI API",
        "version": "1.0.0",
        "docs": "/docs",
    }
