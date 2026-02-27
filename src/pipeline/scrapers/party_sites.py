"""
Party Sites Scraper
Scrapes official party websites
"""

from typing import List, Dict
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
import logging

from .base import BaseScraper, ScraperResult
import src.config as config

logger = logging.getLogger(__name__)


class PartySitesScraper(BaseScraper):
    """
    Scraper for political party websites.
    """
    
    def __init__(self):
        super().__init__("PartySitesScraper")
        self.party_sites = {
            "CHP": "https://chp.org.tr",
            "AKP": "https://www.akparti.org.tr",
            "MHP": "https://mhp.org.tr",
            "İYİ": "https://iyiparti.org.tr",
            "DEM": "https://www.dem.org.tr",
            "SP": "https://saadet.org.tr",
            "ZP": "https://www.zaferpartisi.org.tr",
            "BBP": "https://www.bbp.org.tr",
        }
    
    async def scrape(self, party: str = None, max_results: int = 10) -> List[ScraperResult]:
        """
        Scrape party websites.
        
        Args:
            party: Specific party to scrape (optional)
            max_results: Maximum results per party
            
        Returns:
            List of scraper results
        """
        results = []
        
        parties_to_scrape = (
            {party: self.party_sites[party]} 
            if party and party in self.party_sites 
            else self.party_sites
        )
        
        for party_code, url in parties_to_scrape.items():
            try:
                party_results = await self._scrape_party(party_code, url, max_results)
                results.extend(party_results)
            except Exception as e:
                self.logger.error(f"Error scraping {party_code}: {e}")
        
        return results
    
    async def _scrape_party(self, party: str, url: str, max_results: int) -> List[ScraperResult]:
        """Scrape a single party website."""
        results = []
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                
                async with session.get(
                    url, 
                    timeout=aiohttp.ClientTimeout(total=15),
                    headers=headers
                ) as response:
                    if response.status == 200:
                        text = await response.text()
                        soup = BeautifulSoup(text, "html.parser")
                        
                        for link in soup.find_all("a", href=True)[:max_results]:
                            try:
                                href = link.get("href", "")
                                
                                if not href.startswith("http"):
                                    href = url + href
                                
                                if any(x in href.lower() for x in ["haber", "duyuru", "basin", "aciklama", "program", "tuzuk"]):
                                    title = link.get_text(strip=True)
                                    
                                    if title and len(title) > 10:
                                        result = ScraperResult(
                                            title=title,
                                            content=f"{party} - {title}",
                                            url=href,
                                            source=party,
                                            metadata={
                                                "type": "party_site",
                                                "party": party,
                                            },
                                        )
                                        results.append(result)
                                        
                            except Exception:
                                continue
                                
        except Exception as e:
            self.logger.error(f"Error in _scrape_party for {party}: {e}")
        
        return results
    
    async def get_party_statute(self, party: str) -> str:
        """
        Get party statute URL.
        
        Args:
            party: Party code
            
        Returns:
            URL of the party statute
        """
        party = party.upper()
        
        if party in config.PARTY_PDFS:
            return str(config.PARTY_PDFS[party])
        
        return ""


async def scrape_party_news(party: str = None) -> List[ScraperResult]:
    """
    Convenience function to scrape party news.
    
    Args:
        party: Optional party code
        
    Returns:
        List of party news results
    """
    scraper = PartySitesScraper()
    return await scraper.scrape_with_validation(party=party)
