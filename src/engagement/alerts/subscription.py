"""
Alert Subscription Model
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr
import logging

logger = logging.getLogger(__name__)


class AlertSubscription(BaseModel):
    """Alert subscription model."""
    id: str
    user_id: str
    email: Optional[EmailStr] = None
    parties: List[str] = []
    topics: List[str] = []
    keywords: List[str] = []
    frequency: str = "daily"
    channels: List[str] = ["email"]
    enabled: bool = True
    created_at: datetime
    updated_at: datetime


class AlertTrigger(BaseModel):
    """Alert trigger model."""
    id: str
    subscription_id: str
    trigger_type: str
    message: str
    data: Dict[str, Any] = {}
    created_at: datetime
    sent: bool = False


class UserPreferences(BaseModel):
    """User preferences model."""
    user_id: str
    email: EmailStr
    name: str
    notifications_enabled: bool = True
    email_digest: str = "daily"
    alert_keywords: List[str] = []
    favorite_parties: List[str] = []
    favorite_topics: List[str] = []
    created_at: datetime
    updated_at: datetime


class SubscriptionManager:
    """
    Manages user alert subscriptions.
    """
    
    def __init__(self):
        self.subscriptions: Dict[str, AlertSubscription] = {}
        self.triggers: Dict[str, AlertTrigger] = {}
        self.preferences: Dict[str, UserPreferences] = {}
    
    def create_subscription(
        self,
        user_id: str,
        parties: List[str],
        topics: List[str] = [],
        keywords: List[str] = [],
        frequency: str = "daily",
    ) -> AlertSubscription:
        """Create a new subscription."""
        import uuid
        
        subscription = AlertSubscription(
            id=str(uuid.uuid4()),
            user_id=user_id,
            parties=parties,
            topics=topics,
            keywords=keywords,
            frequency=frequency,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        self.subscriptions[subscription.id] = subscription
        logger.info(f"Created subscription: {subscription.id}")
        
        return subscription
    
    def get_subscription(self, subscription_id: str) -> Optional[AlertSubscription]:
        """Get subscription by ID."""
        return self.subscriptions.get(subscription_id)
    
    def get_user_subscriptions(self, user_id: str) -> List[AlertSubscription]:
        """Get all subscriptions for a user."""
        return [
            sub for sub in self.subscriptions.values()
            if sub.user_id == user_id
        ]
    
    def update_subscription(
        self,
        subscription_id: str,
        parties: Optional[List[str]] = None,
        topics: Optional[List[str]] = None,
        frequency: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> Optional[AlertSubscription]:
        """Update a subscription."""
        sub = self.subscriptions.get(subscription_id)
        if not sub:
            return None
        
        if parties is not None:
            sub.parties = parties
        if topics is not None:
            sub.topics = topics
        if frequency is not None:
            sub.frequency = frequency
        if enabled is not None:
            sub.enabled = enabled
        
        sub.updated_at = datetime.now()
        
        return sub
    
    def delete_subscription(self, subscription_id: str) -> bool:
        """Delete a subscription."""
        if subscription_id in self.subscriptions:
            del self.subscriptions[subscription_id]
            return True
        return False
    
    def create_trigger(
        self,
        subscription_id: str,
        trigger_type: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> AlertTrigger:
        """Create an alert trigger."""
        import uuid
        
        trigger = AlertTrigger(
            id=str(uuid.uuid4()),
            subscription_id=subscription_id,
            trigger_type=trigger_type,
            message=message,
            data=data or {},
            created_at=datetime.now(),
        )
        
        self.triggers[trigger.id] = trigger
        return trigger
    
    def get_pending_triggers(self, limit: int = 100) -> List[AlertTrigger]:
        """Get pending triggers."""
        return [
            t for t in self.triggers.values()
            if not t.sent
        ][:limit]
    
    def mark_trigger_sent(self, trigger_id: str):
        """Mark trigger as sent."""
        if trigger_id in self.triggers:
            self.triggers[trigger_id].sent = True
    
    def save_preferences(self, preferences: UserPreferences):
        """Save user preferences."""
        self.preferences[preferences.user_id] = preferences
    
    def get_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """Get user preferences."""
        return self.preferences.get(user_id)


subscription_manager = SubscriptionManager()
