# Skill karma calculations

from typing import Optional, Dict, Any
from datetime import datetime, UTC
from enum import Enum
from pydantic import BaseModel, Field

from ....models.karma import KarmaTransaction, KarmaTransactionCreate
from ....models.karma_action import KarmaActionType
from ....models.user import UserReference
from ....config.skill_config import SKILL_POINTS, SKILL_RATE_LIMITS, SKILL_CATEGORIES, SERVICE_COMPLETION, REVIEW_THRESHOLDS, VERIFICATION_REQUIREMENTS
from ....config.base_config import QUALITY_MULTIPLIERS, VERIFICATION_MULTIPLIERS, KARMA_DECAY
from ....db.repositories.karma_repository import KarmaRepository

class SkillKarmaService:
    """Service for handling skill-related karma calculations and operations."""
    
    def __init__(self, karma_repository: KarmaRepository):
        self.karma_repository = karma_repository
        
    async def calculate_skill_listing_karma(
        self,
        user: UserReference,
        skill_id: str,
        skill_category: str,
        skill_quality: float = QUALITY_MULTIPLIERS["DEFAULT"],
        market_demand: float = 1.0
    ) -> KarmaTransaction:
        """Calculate karma points for listing a skill."""
        # Get base points from skill category
        category_info = SKILL_CATEGORIES.get(skill_category, {})
        base_points = category_info.get("base_points", SKILL_POINTS["SKILL_LISTING"])
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], skill_quality)
        )
        
        # Apply market demand multiplier
        demand_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], market_demand)
        )
        
        # Calculate final points
        points = base_points * quality_multiplier * demand_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.SKILL_LISTING,
            points=points,
            context_id=skill_id,
            context_type="skill",
            description=f"Listed {skill_category} skill",
            impact_level="STANDARD"
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def calculate_service_completion_karma(
        self,
        user: UserReference,
        service_id: str,
        service_quality: float = QUALITY_MULTIPLIERS["DEFAULT"],
        client_rating: float = 1.0
    ) -> KarmaTransaction:
        """Calculate karma points for completing a service."""
        base_points = SKILL_POINTS["SERVICE_COMPLETION"]
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], service_quality)
        )
        
        # Apply client rating multiplier
        rating_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], client_rating)
        )
        
        # Calculate final points
        points = base_points * quality_multiplier * rating_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.SERVICE_COMPLETION,
            points=points,
            context_id=service_id,
            context_type="service",
            description="Completed a service",
            impact_level="HIGH_IMPACT"
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def calculate_skill_verification_karma(
        self,
        user: UserReference,
        skill_id: str,
        verification_quality: float = QUALITY_MULTIPLIERS["DEFAULT"]
    ) -> KarmaTransaction:
        """Calculate karma points for verifying a skill."""
        base_points = SKILL_POINTS["SKILL_VERIFICATION"]
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], verification_quality)
        )
        
        # Calculate final points
        points = base_points * quality_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.SKILL_VERIFICATION,
            points=points,
            context_id=skill_id,
            context_type="skill",
            description="Verified a skill",
            impact_level="HIGH_IMPACT"
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def calculate_review_karma(
        self,
        user: UserReference,
        service_id: str,
        review_quality: float = QUALITY_MULTIPLIERS["DEFAULT"],
        review_helpfulness: float = 1.0
    ) -> KarmaTransaction:
        """Calculate karma points for providing a service review."""
        base_points = SKILL_POINTS["SERVICE_REVIEW"]
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], review_quality)
        )
        
        # Apply helpfulness multiplier
        helpfulness_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], review_helpfulness)
        )
        
        # Calculate final points
        points = base_points * quality_multiplier * helpfulness_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.SERVICE_REVIEW,
            points=points,
            context_id=service_id,
            context_type="service",
            description="Provided service review",
            impact_level="MINOR"
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
        if action_type == KarmaActionType.SKILL_LISTING:
            return len(actions) < SKILL_RATE_LIMITS["LISTINGS_PER_DAY"]
        elif action_type == KarmaActionType.SERVICE_REVIEW:
            return len(actions) < SKILL_RATE_LIMITS["REVIEWS_PER_DAY"]
        elif action_type == KarmaActionType.SKILL_VERIFICATION:
            return len(actions) < SKILL_RATE_LIMITS["VERIFICATIONS_PER_DAY"]
            
        return True  # No limit for other actions
        
    async def get_user_skill_karma(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> float:
        """Get total skill karma for a user within a date range."""
        return await self.karma_repository.get_user_karma_by_domain(
            user_id,
            "skill",
            start_date,
            end_date
        )
        
    async def get_user_skill_actions(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[KarmaTransaction]:
        """Get all skill karma actions for a user within a date range."""
        return await self.karma_repository.get_user_actions_by_domain(
            user_id,
            "skill",
            start_date,
            end_date
        )
