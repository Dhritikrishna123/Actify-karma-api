# Eco karma calculations

from typing import Optional, Dict, Any
from datetime import datetime, UTC
from enum import Enum
from pydantic import BaseModel, Field

from ....models.karma import KarmaTransaction, KarmaTransactionCreate
from ....models.karma_action import KarmaActionType
from ....models.user import UserReference
from ....config.eco_config import ECO_POINTS, ECO_RATE_LIMITS, CHALLENGE_CATEGORIES, IMPACT_DOCUMENTATION, COMMUNITY_ENGAGEMENT
from ....config.base_config import QUALITY_MULTIPLIERS, SIZE_MULTIPLIERS, KARMA_DECAY
from ....db.repositories.karma_repository import KarmaRepository

class EcoKarmaService:
    """Service for handling eco karma calculations and operations."""
    
    def __init__(self, karma_repository: KarmaRepository):
        self.karma_repository = karma_repository
        
    async def calculate_challenge_participation_karma(
        self,
        user: UserReference,
        challenge_id: str,
        challenge_type: str,
        participation_quality: float = QUALITY_MULTIPLIERS["DEFAULT"],
        impact_score: float = 1.0
    ) -> KarmaTransaction:
        """Calculate karma points for participating in eco-challenges."""
        # Get base points from challenge category
        category_info = CHALLENGE_CATEGORIES.get(challenge_type, {})
        base_points = category_info.get("points", ECO_POINTS["CHALLENGE_PARTICIPATION"])
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], participation_quality)
        )
        
        # Apply impact multiplier
        impact_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], impact_score)
        )
        
        # Calculate final points
        points = base_points * quality_multiplier * impact_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.CHALLENGE_PARTICIPATION,
            points=points,
            context_id=challenge_id,
            context_type="challenge",
            description=f"Participated in {challenge_type} challenge",
            impact_level=category_info.get("impact", "STANDARD")
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def calculate_challenge_creation_karma(
        self,
        user: UserReference,
        challenge_id: str,
        challenge_type: str,
        challenge_quality: float = QUALITY_MULTIPLIERS["DEFAULT"],
        expected_impact: float = 1.0
    ) -> KarmaTransaction:
        """Calculate karma points for creating eco-challenges."""
        base_points = ECO_POINTS["CHALLENGE_CREATION"]
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], challenge_quality)
        )
        
        # Apply expected impact multiplier
        impact_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], expected_impact)
        )
        
        # Calculate final points
        points = base_points * quality_multiplier * impact_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.CHALLENGE_CREATION,
            points=points,
            context_id=challenge_id,
            context_type="challenge",
            description=f"Created {challenge_type} challenge",
            impact_level="HIGH_IMPACT"
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def calculate_impact_documentation_karma(
        self,
        user: UserReference,
        documentation_id: str,
        documentation_quality: float = QUALITY_MULTIPLIERS["DEFAULT"],
        verified_impact: float = 1.0
    ) -> KarmaTransaction:
        """Calculate karma points for documenting environmental impact."""
        base_points = ECO_POINTS["IMPACT_DOCUMENTATION"]
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], documentation_quality)
        )
        
        # Apply verified impact multiplier
        impact_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], verified_impact)
        )
        
        # Calculate final points
        points = base_points * quality_multiplier * impact_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.IMPACT_DOCUMENTATION,
            points=points,
            context_id=documentation_id,
            context_type="documentation",
            description="Documented environmental impact",
            impact_level="HIGH_IMPACT"
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def calculate_community_engagement_karma(
        self,
        user: UserReference,
        engagement_id: str,
        engagement_quality: float = QUALITY_MULTIPLIERS["DEFAULT"],
        community_size: int = 1
    ) -> KarmaTransaction:
        """Calculate karma points for community engagement in eco-challenges."""
        base_points = ECO_POINTS["COMMUNITY_ENGAGEMENT"]
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], engagement_quality)
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
            action_type=KarmaActionType.COMMUNITY_ENGAGEMENT,
            points=points,
            context_id=engagement_id,
            context_type="engagement",
            description="Engaged community in eco-challenge",
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
        if action_type == KarmaActionType.CHALLENGE_CREATION:
            return len(actions) < ECO_RATE_LIMITS["CHALLENGES_PER_DAY"]
        elif action_type == KarmaActionType.CHALLENGE_PARTICIPATION:
            return len(actions) < ECO_RATE_LIMITS["PARTICIPATIONS_PER_DAY"]
        elif action_type == KarmaActionType.IMPACT_DOCUMENTATION:
            return len(actions) < ECO_RATE_LIMITS["DOCUMENTATIONS_PER_DAY"]
            
        return True  # No limit for other actions
        
    async def get_user_eco_karma(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> float:
        """Get total eco karma for a user within a date range."""
        return await self.karma_repository.get_user_karma_by_domain(
            user_id,
            "eco",
            start_date,
            end_date
        )
        
    async def get_user_eco_actions(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[KarmaTransaction]:
        """Get all eco karma actions for a user within a date range."""
        return await self.karma_repository.get_user_actions_by_domain(
            user_id,
            "eco",
            start_date,
            end_date
        )
