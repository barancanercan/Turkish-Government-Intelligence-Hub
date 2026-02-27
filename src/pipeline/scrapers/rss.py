"""
RSS Feed Integration
"""

from typing import List, Dict
import aiohttp
from datetime import datetime
import logging

from ..scrapers.base import BaseScraper, ScraperResult

logger = logging.getLogger(__name__)


class RSSFeedScraper(BaseScraper):
    """
    RSS feed scraper for political news.
    """
    
    def __init__(self):
        super().__init__("RSSFeedScraper")
        self.feeds = [
            {
                "name": "TBMM Haber",
                "url": "https://www.tbmm.gov.tr/haberRSS",
                "category": "parliament",
            },
            {
                "name": "Anadolu Ajansı",
                "url": "https://www.aa.com.tr/rss",
                "category": "news",
            },
            {
                "name": "TRT Haber",
                "url": "https://www.trthaber.com/rss",
                "category": "news",
            },
            {
                "name": "NTV",
                "url": "https://www.ntv.com.tr/feeds/rss",
                "category": "news",
            },
        ]
    
    async def scrape(self, max_results: int = 20) -> List[ScraperResult]:
        """
        Scrape RSS feeds.
        
        Args:
            max_results: Maximum number of results
            
        Returns:
            List of scraper results
        """
        results = []
        
        for feed in self.feeds:
            try:
                feed_results = await self._fetch_feed(feed)
                results.extend(feed_results)
            except Exception as e:
                self.logger.error(f"Error fetching {feed['name']}: {e}")
        
        return results[:max_results]
    
    async def _fetch_feed(self, feed: Dict) -> List[ScraperResult]:
        """Fetch a single RSS feed."""
        results = []
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    feed["url"],
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        text = await response.text()
                        
                        try:
                            import feedparser
                            parsed = feedparser.parse(text)
                            
                            for entry in parsed.entries[:10]:
                                try:
                                    result = ScraperResult(
                                        title=entry.get("title", ""),
                                        content=entry.get("summary", "")[:2000],
                                        url=entry.get("link", ""),
                                        source=feed["name"],
                                        metadata={
                                            "category": feed["category"],
                                            "type": "rss",
                                        },
                                    )
                                    results.append(result)
                                except Exception:
                                    continue
                                    
                        except ImportError:
                            self.logger.warning("feedparser not installed, using basic XML parsing")
                            results = await self._parse_basic_rss(text, feed)
                            
        except Exception as e:
            self.logger.error(f"Error in _fetch_feed: {e}")
        
        return results
    
    async def _parse_basic_rss(self, xml_content: str, feed: Dict) -> List[ScraperResult]:
        """Basic RSS parsing without feedparser."""
        from bs4 import BeautifulSoup
        
        results = []
        soup = BeautifulSoup(xml_content, "xml")
        
        for item in soup.find_all("item")[:10]:
            try:
                title = item.find("title")
                link = item.find("link")
                desc = item.find("description")
                
                if title:
                    result = ScraperResult(
                        title=title.get_text(strip=True),
                        content=desc.get_text(strip=True)[:2000] if desc else "",
                        url=link.get_text(strip=True) if link else "",
                        source=feed["name"],
                        metadata={"type": "rss", "category": feed["category"]},
                    )
                    results.append(result)
            except Exception:
                continue
        
        return results


async def fetch_rss_feeds(max_results: int = 20) -> List[ScraperResult]:
    """
    Convenience function to fetch RSS feeds.
    
    Args:
        max_results: Maximum results
        
    Returns:
        List of RSS results
    """
    scraper = RSSFeedScraper()
    return await scraper.scrape_with_validation(max_results=max_results)
