"""
Query Router
Query, Compare, Analyze endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Optional, AsyncGenerator
import time
import logging
import asyncio
import json

from ..schemas import (
    QueryRequest,
    QueryResponse,
    CompareRequest,
    CompareResponse,
    AnalyzeRequest,
    AnalyzeResponse,
)
from ..services.query_service import QueryService
from ..middleware.auth import get_current_user, verify_api_key

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/query", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user),
    api_key: Optional[str] = Depends(verify_api_key),
):
    """
    Query endpoint for simple questions.
    """
    start_time = time.time()

    try:
        service = QueryService()
        result = await service.process_query(
            question=request.question,
            party=request.party,
            top_k=request.top_k,
            user_id=user_id,
        )

        latency_ms = (time.time() - start_time) * 1000

        return QueryResponse(
            answer=result.get("answer", ""),
            sources=result.get("sources", []),
            citations=result.get("citations", []),
            query_type=result.get("query_type", "simple"),
            latency_ms=latency_ms,
        )

    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare", response_model=CompareResponse)
async def compare(
    request: CompareRequest,
    user_id: str = Depends(get_current_user),
):
    """
    Compare endpoint for party comparisons.
    """
    start_time = time.time()

    try:
        service = QueryService()
        result = await service.process_comparison(
            question=request.question,
            parties=request.parties,
            top_k=request.top_k,
            user_id=user_id,
        )

        latency_ms = (time.time() - start_time) * 1000

        return CompareResponse(
            comparison=result.get("comparison", ""),
            party_positions=result.get("party_positions", {}),
            sources=result.get("sources", []),
            latency_ms=latency_ms,
        )

    except Exception as e:
        logger.error(f"Compare error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    request: AnalyzeRequest,
    user_id: str = Depends(get_current_user),
):
    """
    Deep analysis endpoint.
    """
    start_time = time.time()

    try:
        service = QueryService()
        result = await service.process_analysis(
            question=request.question,
            parties=request.parties or None,
            include_web=request.include_web,
            user_id=user_id,
        )

        latency_ms = (time.time() - start_time) * 1000

        return AnalyzeResponse(
            analysis=result.get("analysis", ""),
            key_findings=result.get("key_findings", []),
            sources=result.get("sources", []),
            web_results=result.get("web_results", []),
            latency_ms=latency_ms,
        )

    except Exception as e:
        logger.error(f"Analyze error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def is_valid_response(text: str) -> bool:
    """Check if response is valid (not garbage/nonsense). Called AFTER clean_response."""
    if not text or len(text.strip()) < 20:
        logger.warning(f"Response too short: {len(text.strip()) if text else 0} chars")
        return False

    # Check for excessive special characters (likely garbage)
    special_ratio = sum(1 for c in text if not c.isalnum() and c not in " \n\t.,!?-:\"'éçğıöşüÇĞİÖŞÜ#*_[]()") / max(len(text), 1)
    if special_ratio > 0.5:
        logger.warning(f"Response has too many special chars: {special_ratio:.2f}")
        return False

    return True


def clean_response(text: str) -> str:
    """Clean and fix response text with proper markdown formatting."""
    import re

    # Remove Chinese characters
    text = re.sub(r"[\u4e00-\u9fff]", "", text)

    # Remove very long repeated characters
    text = re.sub(r"(.)\1{5,}", r"\1\1\1", text)

    # Fix markdown formatting - add newlines before headers
    text = re.sub(r"\s*(#{1,3})\s*", r"\n\n\1 ", text)

    # Fix bullet points - add newline before each dash that follows text
    text = re.sub(r"([.!?:])\s*-\s+", r"\1\n\n- ", text)
    text = re.sub(r"([a-züğışçöA-ZÜĞİŞÇÖ])\s+-\s+", r"\1\n- ", text)

    # Add newline before "Kaynak:" or "Kaynaklar:"
    text = re.sub(r"\s*(Kaynak(?:lar)?:)", r"\n\n\1", text)

    # Add double newline between paragraphs (after period followed by capital)
    text = re.sub(r"\.(\s+)([A-ZÜĞİŞÇÖ])", r".\n\n\2", text)

    # Fix multiple newlines (max 2)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Fix multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Clean up start
    text = text.strip()

    return text


@router.post("/query/stream")
async def stream_query(
    request: QueryRequest,
    user_id: str = Depends(get_current_user),
):
    """
    Streaming query endpoint for real-time responses.
    Uses Server-Sent Events (SSE) for continuous data streaming.
    """

    async def generate() -> AsyncGenerator[str, None]:
        """
        Async generator for SSE streaming.
        Yields processed chunks of the response as they become available.
        """
        try:
            service = QueryService()

            # Process the query and get the complete response
            result = await service.process_query(
                question=request.question,
                party=request.party,
                top_k=request.top_k,
                user_id=user_id,
            )

            answer = result.get("answer", "")
            sources = result.get("sources", [])
            query_type = result.get("query_type", "simple")

            # Clean first, then validate
            if answer:
                answer = clean_response(answer)

            if not answer or not is_valid_response(answer):
                yield f"data: {json.dumps({'content': 'Yanıt oluşturulamadı. Lütfen başka bir soru deneyin.'})}\n\n"
            else:

                # Stream in sentence chunks for better performance
                sentences = answer.replace(". ", ".|").replace("? ", "?|").replace("! ", "!|").split("|")
                for sentence in sentences:
                    if sentence.strip() and len(sentence.strip()) > 2:
                        yield f"data: {json.dumps({'content': sentence.strip() + ' '})}\n\n"
                        await asyncio.sleep(0.05)

            # Send sources as a final chunk
            if sources:
                yield f"data: {json.dumps({'sources': sources})}\n\n"

            # Send metadata
            yield f"data: {json.dumps({'query_type': query_type})}\n\n"

            # Signal completion
            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Stream query error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable Nginx buffering if behind proxy
        },
    )


@router.post("/compare/stream")
async def stream_compare(
    request: CompareRequest,
    user_id: str = Depends(get_current_user),
):
    """
    Streaming compare endpoint for real-time party comparison responses.
    """

    async def generate() -> AsyncGenerator[str, None]:
        """
        Async generator for SSE streaming of comparison results.
        """
        try:
            service = QueryService()

            # Process the comparison
            result = await service.process_comparison(
                question=request.question,
                parties=request.parties,
                top_k=request.top_k,
                user_id=user_id,
            )

            comparison = result.get("comparison", "")
            party_positions = result.get("party_positions", {})
            sources = result.get("sources", [])

            # Clean first, then validate
            if comparison:
                comparison = clean_response(comparison)

            if not comparison or not is_valid_response(comparison):
                yield f"data: {json.dumps({'content': 'Karşılaştırma oluşturulamadı. Lütfen başka bir soru deneyin.'})}\n\n"
            else:
                sentences = comparison.replace(". ", ".|").replace("? ", "?|").replace("! ", "!|").split("|")
                for sentence in sentences:
                    if sentence.strip() and len(sentence.strip()) > 2:
                        yield f"data: {json.dumps({'content': sentence.strip() + ' '})}\n\n"
                        await asyncio.sleep(0.05)

            # Send party positions
            if party_positions:
                yield f"data: {json.dumps({'party_positions': party_positions})}\n\n"

            # Send sources
            if sources:
                yield f"data: {json.dumps({'sources': sources})}\n\n"

            # Signal completion
            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Stream compare error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
