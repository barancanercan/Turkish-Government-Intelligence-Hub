"""
Parties Router
Party information endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List
import logging

from ..schemas import PartyInfo, PartyListResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/parties", response_model=PartyListResponse)
async def list_parties():
    """
    Get list of all available parties.
    """
    from src import config
    
    parties = []
    for party_code, party_data in config.PARTY_INFO.items():
        parties.append(PartyInfo(
            code=party_code,
            name=party_data.get("name", party_code),
            short_name=party_data.get("short", party_code),
            website=party_data.get("website"),
            hex_color=party_data.get("hex_color"),
            ideology=party_data.get("ideology"),
            founded=party_data.get("founded"),
            description=party_data.get("description"),
        ))
    
    return PartyListResponse(parties=parties, total=len(parties))


@router.get("/parties/{party_code}", response_model=PartyInfo)
async def get_party(party_code: str):
    """
    Get detailed information about a specific party.
    """
    from src import config
    
    party_code = party_code.upper()
    
    if party_code not in config.PARTY_INFO:
        raise HTTPException(status_code=404, detail="Party not found")
    
    party_data = config.PARTY_INFO[party_code]
    
    return PartyInfo(
        code=party_code,
        name=party_data.get("name", party_code),
        short_name=party_data.get("short", party_code),
        website=party_data.get("website"),
        hex_color=party_data.get("hex_color"),
        ideology=party_data.get("ideology"),
        founded=party_data.get("founded"),
        description=party_data.get("description"),
    )


@router.get("/topics")
async def list_topics():
    """
    Get list of available topics.
    """
    topics = [
        {"id": "economy", "name": "Ekonomi", "description": "Ekonomi politikası"},
        {"id": "education", "name": "Eğitim", "description": "Eğitim politikası"},
        {"id": "health", "name": "Sağlık", "description": "Sağlık politikası"},
        {"id": "foreign_policy", "name": "Dış Politika", "description": "Dış politika"},
        {"id": "environment", "name": "Çevre", "description": "Çevre politikası"},
        {"id": "security", "name": "Güvenlik", "description": "Güvenlik politikası"},
    ]
    return {"topics": topics, "total": len(topics)}
