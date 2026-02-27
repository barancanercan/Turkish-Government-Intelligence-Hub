"""
Pipeline Scheduler
Daily cron job for data updates
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class PipelineScheduler:
    """
    Scheduler for running pipeline tasks.
    """
    
    def __init__(self):
        self.tasks = []
        self.last_run = None
        self.run_history = []
    
    def add_task(self, name: str, func, schedule: str = "daily"):
        """
        Add a task to the scheduler.
        
        Args:
            name: Task name
            func: Async function to run
            schedule: Schedule type (daily, hourly, etc.)
        """
        self.tasks.append({
            "name": name,
            "func": func,
            "schedule": schedule,
        })
        logger.info(f"Added task: {name} ({schedule})")
    
    async def run_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single task.
        
        Args:
            task: Task dictionary
            
        Returns:
            Result dictionary
        """
        start_time = datetime.now()
        
        try:
            logger.info(f"Running task: {task['name']}")
            
            result = await task["func"]()
            
            duration = (datetime.now() - start_time).total_seconds()
            
            return {
                "task": task["name"],
                "status": "success",
                "duration": duration,
                "result": result,
                "timestamp": datetime.now().isoformat(),
            }
            
        except Exception as e:
            logger.error(f"Task {task['name']} failed: {e}")
            
            return {
                "task": task["name"],
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
    
    async def run_all(self) -> List[Dict[str, Any]]:
        """
        Run all scheduled tasks.
        
        Returns:
            List of results
        """
        logger.info(f"Running {len(self.tasks)} tasks")
        
        results = []
        
        for task in self.tasks:
            result = await self.run_task(task)
            results.append(result)
            self.run_history.append(result)
        
        self.last_run = datetime.now()
        
        return results
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get run history."""
        return self.run_history[-50:]


async def daily_news_scrape():
    """Daily news scraping task."""
    from ..scrapers import scrape_news
    
    results = await scrape_news(max_results=50)
    
    logger.info(f"Scraped {len(results)} news items")
    
    return {"scraped": len(results)}


async def daily_party_scrape():
    """Daily party news scraping task."""
    from ..scrapers import scrape_party_news
    
    results = await scrape_party_news()
    
    logger.info(f"Scraped {len(results)} party items")
    
    return {"scraped": len(results)}


async def daily_rss_update():
    """Daily RSS feed update task."""
    from ..scrapers import fetch_rss_feeds
    
    results = await fetch_rss_feeds(max_results=30)
    
    logger.info(f"Updated {len(results)} RSS items")
    
    return {"updated": len(results)}


async def daily_vector_update():
    """Daily vector store update task."""
    from .storage.vector_updater import VectorUpdater
    
    logger.info("Running daily vector update")
    
    return {"updated": 0}


def create_daily_scheduler() -> PipelineScheduler:
    """
    Create the daily scheduler with all tasks.
    
    Returns:
        Configured scheduler
    """
    scheduler = PipelineScheduler()
    
    scheduler.add_task("daily_news", daily_news_scrape, "daily")
    scheduler.add_task("daily_party", daily_party_scrape, "daily")
    scheduler.add_task("daily_rss", daily_rss_update, "daily")
    scheduler.add_task("daily_vector", daily_vector_update, "daily")
    
    return scheduler


async def run_daily_pipeline():
    """
    Run the daily pipeline.
    
    Returns:
        Pipeline results
    """
    scheduler = create_daily_scheduler()
    results = await scheduler.run_all()
    
    return results
