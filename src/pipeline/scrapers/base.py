"""
Base Scraper Class
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import hashlib

logger = logging.getLogger(__name__)


class ScraperResult:
    """Result from a scraper."""
    
    def __init__(
        self,
        title: str,
        content: str,
        url: str,
        source: str,
        published_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.title = title
        self.content = content
        self.url = url
        self.source = source
        self.published_at = published_at or datetime.now()
        self.metadata = metadata or {}
        self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique ID for the content."""
        content_hash = hashlib.md5(
            f"{self.url}{self.title}".encode()
        ).hexdigest()
        return content_hash[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "source": self.source,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "metadata": self.metadata,
        }


class BaseScraper(ABC):
    """
    Abstract base class for scrapers.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    @abstractmethod
    async def scrape(self, **kwargs) -> List[ScraperResult]:
        """
        Scrape data from source.
        
        Returns:
            List of ScraperResult objects
        """
        pass
    
    async def run(self, **kwargs) -> List[ScraperResult]:
        """
        Run the scraper with error handling.
        """
        try:
            self.logger.info(f"Starting {self.name} scraper")
            results = await self.scrape(**kwargs)
            self.logger.info(f"Completed {self.name}: {len(results)} results")
            return results
        except Exception as e:
            self.logger.error(f"Error in {self.name}: {e}")
            return []
    
    def validate_result(self, result: ScraperResult) -> bool:
        """
        Validate a scraper result.
        
        Args:
            result: Result to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not result.title or len(result.title) < 5:
            return False
        if not result.content or len(result.content) < 20:
            return False
        if not result.url or not result.url.startswith("http"):
            return False
        return True
    
    async def scrape_with_validation(self, **kwargs) -> List[ScraperResult]:
        """
        Scrape and validate results.
        """
        results = await self.run(**kwargs)
        valid_results = [r for r in results if self.validate_result(r)]
        self.logger.info(f"Valid results: {len(valid_results)}/{len(results)}")
        return valid_results
