"""
News Scraper
Scrapes news from Turkish news sources
"""

from typing import List
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
import logging

from .base import BaseScraper, ScraperResult

logger = logging.getLogger(__name__)


class NewsScraper(BaseScraper):
    """
    Scraper for Turkish news sites.
    """
    
    def __init__(self):
        super().__init__("NewsScraper")
        self.news_sources = [
            {
                "name": "Hürriyet",
                "url": "https://www.hurriyet.com.tr",
                "rss": "https://www.hurriyet.com.tr/rss/son_dakika",
            },
            {
                "name": "Sözcü",
                "url": "https://www.sozcu.com.tr",
                "rss": "https://www.sozcu.com.tr/feeds",
            },
            {
                "name": "Cumhuriyet",
                "url": "https://www.cumhuriyet.com.tr",
                "rss": "https://www.cumhuriyet.com.tr/rss",
            },
            {
                "name": "Milliyet",
                "url": "https://www.milliyet.com.tr",
                "rss": "https://www.milliyet.com.tr/rss/rss_25.xml",
            },
            {
                "name": "Sabah",
                "url": "https://www.sabah.com.tr",
                "rss": "https://www.sabah.com.tr/rss",
            },
        ]
    
    async def scrape(self, max_results: int = 20, keyword: str = None) -> List[ScraperResult]:
        """
        Scrape news from Turkish news sources.
        
        Args:
            max_results: Maximum number of results
            keyword: Optional keyword to filter news
            
        Returns:
            List of scraper results
        """
        results = []
        
        for source in self.news_sources:
            try:
                source_results = await self._scrape_source(source, keyword)
                results.extend(source_results)
                
                if len(results) >= max_results:
                    break
                    
            except Exception as e:
                self.logger.error(f"Error scraping {source['name']}: {e}")
        
        return results[:max_results]
    
    async def _scrape_source(self, source: dict, keyword: str = None) -> List[ScraperResult]:
        """Scrape a single news source."""
        results = []
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    source["rss"], 
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        text = await response.text()
                        results = self._parse_rss(text, source["name"], keyword)
                        
        except Exception as e:
            self.logger.warning(f"RSS failed for {source['name']}, trying HTML: {e}")
            try:
                results = await self._scrape_html(source, keyword)
            except Exception as e2:
                self.logger.error(f"HTML scrape failed: {e2}")
        
        return results
    
    def _parse_rss(self, xml_content: str, source_name: str, keyword: str = None) -> List[ScraperResult]:
        """Parse RSS feed."""
        results = []
        soup = BeautifulSoup(xml_content, "xml")
        
        for item in soup.find_all("item")[:10]:
            try:
                title = item.find("title").get_text(strip=True) if item.find("title") else ""
                link = item.find("link").get_text(strip=True) if item.find("link") else ""
                description = item.find("description").get_text(strip=True) if item.find("description") else ""
                pub_date = item.find("pubDate").get_text(strip=True) if item.find("pubDate") else None
                
                if keyword and keyword.lower() not in title.lower():
                    continue
                
                content = f"{title}\n\n{description}"[:2000]
                
                result = ScraperResult(
                    title=title,
                    content=content,
                    url=link,
                    source=source_name,
                    published_at=self._parse_date(pub_date) if pub_date else None,
                    metadata={"type": "news"},
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.error(f"Error parsing RSS item: {e}")
        
        return results
    
    async def _scrape_html(self, source: dict, keyword: str = None) -> List[ScraperResult]:
        """Fallback HTML scraping."""
        results = []
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    source["url"],
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        text = await response.text()
                        soup = BeautifulSoup(text, "html.parser")
                        
                        for article in soup.find_all("article")[:10]:
                            try:
                                title_elem = article.find("h2") or article.find("h3")
                                link_elem = article.find("a")
                                
                                if not title_elem or not link_elem:
                                    continue
                                
                                title = title_elem.get_text(strip=True)
                                link = link_elem.get("href", "")
                                
                                if not link.startswith("http"):
                                    link = source["url"] + link
                                
                                if keyword and keyword.lower() not in title.lower():
                                    continue
                                
                                result = ScraperResult(
                                    title=title,
                                    content=title,
                                    url=link,
                                    source=source["name"],
                                    metadata={"type": "news"},
                                )
                                
                                results.append(result)
                                
                            except Exception as e:
                                continue
                                
        except Exception as e:
            self.logger.error(f"HTML scrape error: {e}")
        
        return results
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime."""
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_str)
        except:
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except:
                return datetime.now()


async def scrape_news(keyword: str = None, max_results: int = 20) -> List[ScraperResult]:
    """
    Convenience function to scrape news.
    
    Args:
        keyword: Optional keyword to filter
        max_results: Maximum results
        
    Returns:
        List of news results
    """
    scraper = NewsScraper()
    return await scraper.scrape_with_validation(keyword=keyword, max_results=max_results)
