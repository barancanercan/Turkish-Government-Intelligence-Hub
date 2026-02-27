"""
Data Cleaners
"""

from typing import List
import re
import logging

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """
    Clean text for processing.
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    text = re.sub(r'\s+', ' ', text)
    
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    text = text.strip()
    
    return text


def remove_html_tags(text: str) -> str:
    """
    Remove HTML tags from text.
    
    Args:
        text: Text with HTML
        
    Returns:
        Clean text
    """
    if not text:
        return ""
    
    text = re.sub(r'<[^>]+>', '', text)
    
    text = re.sub(r'&[a-zA-Z]+;', ' ', text)
    
    return clean_text(text)


def extract_dates(text: str) -> List[str]:
    """
    Extract dates from text.
    
    Args:
        text: Text to search
        
    Returns:
        List of found dates
    """
    date_patterns = [
        r'\d{1,2}/\d{1,2}/\d{4}',
        r'\d{1,2}-\d{1,2}-\d{4}',
        r'\d{1,2}\s+\w+\s+\d{4}',
    ]
    
    dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        dates.extend(matches)
    
    return dates


def truncate_text(text: str, max_length: int = 2000) -> str:
    """
    Truncate text to max length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


class DataCleaner:
    """
    Data cleaning pipeline.
    """
    
    def __init__(self):
        self.stats = {
            "processed": 0,
            "cleaned": 0,
            "errors": 0,
        }
    
    def clean(self, data: dict) -> dict:
        """
        Clean a single data item.
        
        Args:
            data: Raw data item
            
        Returns:
            Cleaned data
        """
        self.stats["processed"] += 1
        
        try:
            if "title" in data:
                data["title"] = clean_text(remove_html_tags(data["title"]))
            
            if "content" in data:
                data["content"] = clean_text(remove_html_tags(data["content"]))
            
            if "url" in data:
                data["url"] = clean_text(data["url"])
            
            self.stats["cleaned"] += 1
            
        except Exception as e:
            logger.error(f"Cleaning error: {e}")
            self.stats["errors"] += 1
        
        return data
    
    def clean_batch(self, data_items: List[dict]) -> List[dict]:
        """
        Clean a batch of data.
        
        Args:
            data_items: List of raw data items
            
        Returns:
            List of cleaned data
        """
        return [self.clean(item) for item in data_items]
    
    def get_stats(self) -> dict:
        """Get cleaning statistics."""
        return self.stats.copy()
