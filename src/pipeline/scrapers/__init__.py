"""
Scrapers Package
"""

from .base import BaseScraper, ScraperResult
from .news import NewsScraper, scrape_news
from .party_sites import PartySitesScraper, scrape_party_news
from .rss import RSSFeedScraper, fetch_rss_feeds

__all__ = [
    "BaseScraper",
    "ScraperResult",
    "NewsScraper",
    "scrape_news",
    "PartySitesScraper",
    "scrape_party_news",
    "RSSFeedScraper",
    "fetch_rss_feeds",
]
