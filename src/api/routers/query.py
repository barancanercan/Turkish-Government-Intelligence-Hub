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
    QueryRequest, QueryResponse,
    CompareRequest, CompareResponse,
    AnalyzeRequest, AnalyzeResponse,
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

            if not answer:
                yield f"data: {json.dumps({'content': 'Yanıt oluşturulamadı.'})}\n\n"
            else:
                # Stream in sentence chunks for better performance
                sentences = answer.replace('. ', '.|').replace('? ', '?|').replace('! ', '!|').split('|')
                for sentence in sentences:
                    if sentence.strip():
                        yield f"data: {json.dumps({'content': sentence.strip() + ' '})}\n\n"
                        await asyncio.sleep(0.05)  # Slightly longer delay for sentence chunks

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

            # Stream in sentence chunks for better performance
            if not comparison:
                yield f"data: {json.dumps({'content': 'Karşılaştırma oluşturulamadı.'})}\n\n"
            else:
                sentences = comparison.replace('. ', '.|').replace('? ', '?|').replace('! ', '!|').split('|')
                for sentence in sentences:
                    if sentence.strip():
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
