"""
Query History & Saved Queries
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class QueryHistory(BaseModel):
    """Query history entry."""
    id: str
    user_id: str
    query: str
    answer: Optional[str] = None
    sources: List[str] = []
    query_type: str = "simple"
    latency_ms: float = 0.0
    created_at: datetime


class SavedQuery(BaseModel):
    """Saved query."""
    id: str
    user_id: str
    name: str
    query: str
    description: Optional[str] = None
    party_filter: Optional[str] = None
    tags: List[str] = []
    is_public: bool = False
    created_at: datetime
    updated_at: datetime


class QueryHistoryManager:
    """
    Manages query history and saved queries.
    """
    
    def __init__(self):
        self.history: Dict[str, QueryHistory] = {}
        self.saved_queries: Dict[str, SavedQuery] = {}
    
    def add_history(
        self,
        user_id: str,
        query: str,
        answer: Optional[str] = None,
        sources: Optional[List[str]] = None,
        query_type: str = "simple",
        latency_ms: float = 0.0,
    ) -> QueryHistory:
        """Add query to history."""
        import uuid
        
        history = QueryHistory(
            id=str(uuid.uuid4()),
            user_id=user_id,
            query=query,
            answer=answer,
            sources=sources or [],
            query_type=query_type,
            latency_ms=latency_ms,
            created_at=datetime.now(),
        )
        
        self.history[history.id] = history
        logger.info(f"Added query to history: {history.id}")
        
        return history
    
    def get_user_history(
        self,
        user_id: str,
        limit: int = 50,
    ) -> List[QueryHistory]:
        """Get user's query history."""
        user_history = [
            h for h in self.history.values()
            if h.user_id == user_id
        ]
        
        user_history.sort(key=lambda x: x.created_at, reverse=True)
        
        return user_history[:limit]
    
    def search_history(
        self,
        user_id: str,
        query: str,
        limit: int = 10,
    ) -> List[QueryHistory]:
        """Search in user's query history."""
        user_history = self.get_user_history(user_id, limit=100)
        
        query_lower = query.lower()
        
        results = [
            h for h in user_history
            if query_lower in h.query.lower()
        ]
        
        return results[:limit]
    
    def save_query(
        self,
        user_id: str,
        name: str,
        query: str,
        description: Optional[str] = None,
        party_filter: Optional[str] = None,
        tags: Optional[List[str]] = None,
        is_public: bool = False,
    ) -> SavedQuery:
        """Save a query."""
        import uuid
        
        saved = SavedQuery(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=name,
            query=query,
            description=description,
            party_filter=party_filter,
            tags=tags or [],
            is_public=is_public,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        self.saved_queries[saved.id] = saved
        logger.info(f"Saved query: {saved.id}")
        
        return saved
    
    def get_saved_queries(
        self,
        user_id: str,
        include_public: bool = True,
    ) -> List[SavedQuery]:
        """Get user's saved queries."""
        queries = [
            q for q in self.saved_queries.values()
            if q.user_id == user_id or (include_public and q.is_public)
        ]
        
        queries.sort(key=lambda x: x.created_at, reverse=True)
        
        return queries
    
    def update_saved_query(
        self,
        query_id: str,
        user_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Optional[SavedQuery]:
        """Update a saved query."""
        query = self.saved_queries.get(query_id)
        
        if not query or query.user_id != user_id:
            return None
        
        if name is not None:
            query.name = name
        if description is not None:
            query.description = description
        if tags is not None:
            query.tags = tags
        
        query.updated_at = datetime.now()
        
        return query
    
    def delete_saved_query(self, query_id: str, user_id: str) -> bool:
        """Delete a saved query."""
        query = self.saved_queries.get(query_id)
        
        if not query or query.user_id != user_id:
            return False
        
        del self.saved_queries[query_id]
        
        return True
    
    def get_popular_tags(self, limit: int = 20) -> List[tuple]:
        """Get popular tags from saved queries."""
        tag_counts: Dict[str, int] = {}
        
        for query in self.saved_queries.values():
            for tag in query.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_tags[:limit]


query_history_manager = QueryHistoryManager()
