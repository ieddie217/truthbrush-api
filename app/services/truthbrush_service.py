from datetime import datetime, timezone
from typing import List, Optional
from truthbrush.api import Api
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class TruthbrushService:
    """Service layer for interacting with Truth Social via truthbrush."""
    
    def __init__(self):
        """Initialize the truthbrush API client."""
        self.api = Api(
            username=settings.TRUTHSOCIAL_USERNAME,
            password=settings.TRUTHSOCIAL_PASSWORD,
            token=settings.TRUTHSOCIAL_TOKEN
        )
    
    def get_user_statuses(
        self,
        username: str,
        created_after: Optional[str] = None,
        replies: bool = False,
        pinned: bool = False
    ) -> List[dict]:
        """
        Get statuses for a user with optional filtering.
        
        Args:
            username: Truth Social username
            created_after: ISO date string (e.g., "2025-07-23")
            replies: Include replies in results
            pinned: Only return pinned posts
            
        Returns:
            List of status objects
        """
        # Parse and validate created_after date
        dt = None
        if created_after:
            try:
                dt = datetime.fromisoformat(created_after)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
            except ValueError as e:
                raise ValueError(f"Invalid created_after format: {e}")
        
        # Get statuses from truthbrush
        try:
            statuses = list(self.api.pull_statuses(
                username=username,
                created_after=dt,
                replies=replies,
                pinned=pinned
            ))
            return statuses
        except Exception as e:
            logger.error(f"Error fetching statuses for {username}: {e}")
            raise 