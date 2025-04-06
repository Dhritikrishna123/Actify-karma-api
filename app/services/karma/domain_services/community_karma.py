# Community karma calculations

from typing import Optional, Dict, Any
from datetime import datetime, UTC
from enum import Enum
from pydantic import BaseModel, Field

from ....models.karma import KarmaTransaction, KarmaTransactionCreate
from ....models.karma_action import KarmaActionType
from ....models.user import UserReference
from ....config.community_config import COMMUNITY_POINTS, COMMUNITY_RATE_LIMITS, COMMUNITY_TYPES, EVENT_REQUIREMENTS, MENTORSHIP_REQUIREMENTS, MODERATION_THRESHOLDS
from ....config.base_config import QUALITY_MULTIPLIERS, SIZE_MULTIPLIERS, KARMA_DECAY
from ....db.repositories.karma_repository import KarmaRepository

class CommunityKarmaService:
    """Service for handling community-related karma calculations and operations."""
    
    def __init__(self, karma_repository: KarmaRepository):
        self.karma_repository = karma_repository
        
    async def calculate_community_creation_karma(
        self,
        user: UserReference,
        community_id: str,
        community_type: str,
        community_quality: float = QUALITY_MULTIPLIERS["DEFAULT"],
        community_size: int = 1
    ) -> KarmaTransaction:
        """Calculate karma points for creating a community space."""
        # Get base points from community type
        type_info = COMMUNITY_TYPES.get(community_type, {})
        base_points = type_info.get("base_points", COMMUNITY_POINTS["COMMUNITY_CREATION"])
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], community_quality)
        )
        
        # Apply community size multiplier
        size_multiplier = min(
            SIZE_MULTIPLIERS["MAX_MULTIPLIER"],
            1.0 + (community_size / SIZE_MULTIPLIERS["COMMUNITY_SIZE_DIVISOR"])
        )
        
        # Calculate final points
        points = base_points * quality_multiplier * size_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.COMMUNITY_CREATION,
            points=points,
            context_id=community_id,
            context_type="community",
            description=f"Created {community_type} community",
            impact_level="HIGH_IMPACT"
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def calculate_event_organization_karma(
        self,
        user: UserReference,
        event_id: str,
        event_quality: float = QUALITY_MULTIPLIERS["DEFAULT"],
        attendance: int = 1
    ) -> KarmaTransaction:
        """Calculate karma points for organizing a community event."""
        base_points = COMMUNITY_POINTS["EVENT_ORGANIZATION"]
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], event_quality)
        )
        
        # Apply attendance multiplier
        attendance_multiplier = min(
            SIZE_MULTIPLIERS["MAX_MULTIPLIER"],
            1.0 + (attendance / SIZE_MULTIPLIERS["EVENT_ATTENDANCE_DIVISOR"])
        )
        
        # Calculate final points
        points = base_points * quality_multiplier * attendance_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.EVENT_ORGANIZATION,
            points=points,
            context_id=event_id,
            context_type="event",
            description="Organized a community event",
            impact_level="STANDARD"
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def calculate_mentorship_karma(
        self,
        user: UserReference,
        mentee_id: str,
        mentorship_quality: float = QUALITY_MULTIPLIERS["DEFAULT"],
        mentee_progress: float = 1.0
    ) -> KarmaTransaction:
        """Calculate karma points for mentoring community members."""
        base_points = COMMUNITY_POINTS["MENTORSHIP"]
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], mentorship_quality)
        )
        
        # Apply mentee progress multiplier
        progress_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], mentee_progress)
        )
        
        # Calculate final points
        points = base_points * quality_multiplier * progress_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.MENTORSHIP,
            points=points,
            context_id=mentee_id,
            context_type="mentorship",
            description="Mentored a community member",
            impact_level="HIGH_IMPACT"
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def calculate_moderation_karma(
        self,
        user: UserReference,
        community_id: str,
        moderation_quality: float = QUALITY_MULTIPLIERS["DEFAULT"],
        community_health: float = 1.0
    ) -> KarmaTransaction:
        """Calculate karma points for community moderation activities."""
        base_points = COMMUNITY_POINTS["COMMUNITY_MODERATION"]
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], moderation_quality)
        )
        
        # Apply community health multiplier
        health_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], community_health)
        )
        
        # Calculate final points
        points = base_points * quality_multiplier * health_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.COMMUNITY_MODERATION,
            points=points,
            context_id=community_id,
            context_type="community",
            description="Moderated community activities",
            impact_level="STANDARD"
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def check_daily_limits(
        self,
        user_id: str,
        action_type: KarmaActionType
    ) -> bool:
        """Check if user has exceeded daily limits for an action."""
        # Get user's actions for today
        today = datetime.now(UTC).date()
        actions = await self.karma_repository.get_user_actions_today(
            user_id,
            action_type,
            today
        )
        
        # Check against rate limits
        if action_type == KarmaActionType.COMMUNITY_CREATION:
            return len(actions) < COMMUNITY_RATE_LIMITS["COMMUNITIES_PER_DAY"]
        elif action_type == KarmaActionType.EVENT_ORGANIZATION:
            return len(actions) < COMMUNITY_RATE_LIMITS["EVENTS_PER_DAY"]
        elif action_type == KarmaActionType.MENTORSHIP:
            return len(actions) < COMMUNITY_RATE_LIMITS["MENTORSHIPS_PER_DAY"]
            
        return True  # No limit for other actions
        
    async def get_user_community_karma(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> float:
        """Get total community karma for a user within a date range."""
        return await self.karma_repository.get_user_karma_by_domain(
            user_id,
            "community",
            start_date,
            end_date
        )
        
    async def get_user_community_actions(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[KarmaTransaction]:
        """Get all community karma actions for a user within a date range."""
        return await self.karma_repository.get_user_actions_by_domain(
            user_id,
            "community",
            start_date,
            end_date
        )
