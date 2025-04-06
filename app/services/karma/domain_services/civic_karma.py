# Civic karma calculations

from typing import Optional, Dict, Any
from datetime import datetime, UTC
from enum import Enum
from pydantic import BaseModel, Field

from ....models.karma import KarmaTransaction, KarmaTransactionCreate
from ....models.karma_action import KarmaActionType
from ....models.user import UserReference
from ....config.civic_config import CIVIC_POINTS, CIVIC_RATE_LIMITS, CIVIC_QUALITY_THRESHOLDS, REPORT_CATEGORIES
from ....config.base_config import QUALITY_MULTIPLIERS, TIME_MULTIPLIERS, KARMA_DECAY
from ....db.repositories.karma_repository import KarmaRepository

class CivicKarmaService:
    """Service for handling civic karma calculations and operations."""
    
    def __init__(self, karma_repository: KarmaRepository):
        self.karma_repository = karma_repository
        
    async def calculate_report_creation_karma(
        self,
        user: UserReference,
        report_id: str,
        report_category: str,
        report_quality: float = QUALITY_MULTIPLIERS["DEFAULT"]
    ) -> KarmaTransaction:
        """Calculate karma points for creating a report."""
        # Get base points from category
        category_info = REPORT_CATEGORIES.get(report_category, {})
        base_points = category_info.get("points", CIVIC_POINTS["REPORT_CREATION"])
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], report_quality)
        )
        
        # Calculate final points
        points = base_points * quality_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.REPORT_CREATION,
            points=points,
            context_id=report_id,
            context_type="report",
            description=f"Created {report_category} report",
            impact_level=category_info.get("impact", "STANDARD")
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def calculate_report_verification_karma(
        self,
        user: UserReference,
        report_id: str,
        verification_quality: float = QUALITY_MULTIPLIERS["DEFAULT"]
    ) -> KarmaTransaction:
        """Calculate karma points for verifying a report."""
        base_points = CIVIC_POINTS["REPORT_VERIFICATION"]
        
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
            action_type=KarmaActionType.REPORT_VERIFICATION,
            points=points,
            context_id=report_id,
            context_type="report",
            description="Verified report",
            impact_level="STANDARD"
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def calculate_report_resolution_karma(
        self,
        user: UserReference,
        report_id: str,
        resolution_quality: float = QUALITY_MULTIPLIERS["DEFAULT"],
        resolution_time: Optional[float] = None
    ) -> KarmaTransaction:
        """Calculate karma points for resolving a report."""
        base_points = CIVIC_POINTS["REPORT_RESOLUTION"]
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], resolution_quality)
        )
        
        # Apply time bonus if resolution was quick
        time_multiplier = 1.0
        if resolution_time and resolution_time < TIME_MULTIPLIERS["QUICK_RESOLUTION_THRESHOLD"]:
            time_multiplier = TIME_MULTIPLIERS["QUICK_RESOLUTION_BONUS"]
            
        # Calculate final points
        points = base_points * quality_multiplier * time_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.REPORT_RESOLUTION,
            points=points,
            context_id=report_id,
            context_type="report",
            description="Resolved report",
            impact_level="HIGH_IMPACT"
        )
        
        return await self.karma_repository.create_transaction(transaction)
        
    async def calculate_endorsement_karma(
        self,
        user: UserReference,
        report_id: str,
        endorsement_quality: float = QUALITY_MULTIPLIERS["DEFAULT"]
    ) -> KarmaTransaction:
        """Calculate karma points for endorsing a report."""
        base_points = CIVIC_POINTS["ENDORSEMENT"]
        
        # Apply quality multiplier
        quality_multiplier = max(
            QUALITY_MULTIPLIERS["MIN"],
            min(QUALITY_MULTIPLIERS["MAX"], endorsement_quality)
        )
        
        # Calculate final points
        points = base_points * quality_multiplier
        
        # Create transaction
        transaction = KarmaTransactionCreate(
            user=user,
            action_type=KarmaActionType.REPORT_ENDORSEMENT,
            points=points,
            context_id=report_id,
            context_type="report",
            description="Endorsed report",
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
        if action_type == KarmaActionType.REPORT_CREATION:
            return len(actions) < CIVIC_RATE_LIMITS["REPORTS_PER_DAY"]
        elif action_type == KarmaActionType.REPORT_ENDORSEMENT:
            return len(actions) < CIVIC_RATE_LIMITS["ENDORSEMENTS_PER_DAY"]
        elif action_type == KarmaActionType.REPORT_VERIFICATION:
            return len(actions) < CIVIC_RATE_LIMITS["VERIFICATIONS_PER_DAY"]
            
        return True  # No limit for other actions
        
    async def get_user_civic_karma(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> float:
        """Get total civic karma for a user within a date range."""
        return await self.karma_repository.get_user_karma_by_domain(
            user_id,
            "civic",
            start_date,
            end_date
        )
        
    async def get_user_civic_actions(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[KarmaTransaction]:
        """Get all civic karma actions for a user within a date range."""
        return await self.karma_repository.get_user_actions_by_domain(
            user_id,
            "civic",
            start_date,
            end_date
        )
