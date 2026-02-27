"""
Alert System
Slack/Discord webhooks and cost alerts
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import aiohttp

logger = logging.getLogger(__name__)


class AlertManager:
    """
    Alert manager for notifications.
    """
    
    def __init__(self):
        self.webhooks = {
            "slack": None,
            "discord": None,
        }
        self.cost_threshold = 100.0
        self.daily_cost = 0.0
        self.alert_history = []
    
    def set_webhook(self, platform: str, url: str):
        """
        Set webhook URL.
        
        Args:
            platform: "slack" or "discord"
            url: Webhook URL
        """
        self.webhooks[platform] = url
        logger.info(f"Webhook set for {platform}")
    
    def set_cost_threshold(self, threshold: float):
        """Set daily cost threshold."""
        self.cost_threshold = threshold
    
    async def send_alert(
        self,
        message: str,
        level: str = "info",
        platform: str = "slack",
    ):
        """
        Send an alert.
        
        Args:
            message: Alert message
            level: Alert level (info, warning, error)
            platform: Platform (slack, discord)
        """
        webhook_url = self.webhooks.get(platform)
        if not webhook_url:
            logger.warning(f"No webhook configured for {platform}")
            return
        
        payload = {
            "content": message,
            "username": "MIZAN-AI Alert",
            "avatar_url": "https://example.com/mizan-ai.png",
        }
        
        if platform == "slack":
            payload = {
                "text": message,
                "username": "MIZAN-AI Alert",
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    if response.status == 204:
                        logger.info(f"Alert sent to {platform}")
                    else:
                        logger.warning(f"Alert failed: {response.status}")
        except Exception as e:
            logger.error(f"Alert error: {e}")
        
        self.alert_history.append({
            "message": message,
            "level": level,
            "platform": platform,
            "timestamp": datetime.now().isoformat(),
        })
    
    def check_cost_threshold(self, current_cost: float) -> bool:
        """
        Check if cost exceeds threshold.
        
        Args:
            current_cost: Current daily cost
            
        Returns:
            True if alert should be sent
        """
        self.daily_cost = current_cost
        
        if current_cost >= self.cost_threshold:
            return True
        
        if current_cost >= self.cost_threshold * 0.8:
            return True
        
        return False
    
    async def send_cost_alert(self, current_cost: float):
        """Send cost threshold alert."""
        if self.check_cost_threshold(current_cost):
            message = (
                f"Uyarı: Günlük maliyet eşiği aşıldı!\n"
                f"Mevcut maliyet: ${current_cost:.2f}\n"
                threshold: ${self.cost_threshold:.2f}"
            )
            await self.send_alert(message, level="warning")
    
    def get_alert_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent alert history."""
        return self.alert_history[-limit:]


alert_manager = AlertManager()


async def send_slack_alert(message: str, level: str = "info"):
    """Convenience function to send Slack alert."""
    await alert_manager.send_alert(message, level, "slack")


async def send_discord_alert(message: str, level: str = "info"):
    """Convenience function to send Discord alert."""
    await alert_manager.send_alert(message, level, "discord")
