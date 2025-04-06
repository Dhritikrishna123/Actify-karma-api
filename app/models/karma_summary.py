from typing import Optional, Dict
from datetime import datetime, UTC, timedelta
from pydantic import BaseModel, Field

from .base import BaseDBModel
from .user import UserReference

class KarmaSummary(BaseDBModel):
    """Model for tracking user karma statistics and status"""
    # User Reference
    user: UserReference = Field(
        ...,
        description="User this summary belongs to"
    )
    
    # Current Status
    total_points: float = Field(
        default=0.0,
        description="Total karma points earned"
    )
    current_level: int = Field(
        default=1,
        description="Current karma level"
    )
    level_progress: float = Field(
        default=0.0,
        description="Progress to next level (0-100)"
    )
    
    # Statistics
    total_actions: int = Field(
        default=0,
        description="Total number of karma-earning actions"
    )
    positive_actions: int = Field(
        default=0,
        description="Number of positive karma actions"
    )
    negative_actions: int = Field(
        default=0,
        description="Number of negative karma actions"
    )
    
    # Action Type Breakdown
    action_breakdown: Dict[str, int] = Field(
        default_factory=dict,
        description="Breakdown of actions by type"
    )
    
    # Streaks and Achievements
    current_streak: int = Field(
        default=0,
        description="Current streak of positive actions"
    )
    longest_streak: int = Field(
        default=0,
        description="Longest streak of positive actions"
    )
    achievements: Dict[str, bool] = Field(
        default_factory=dict,
        description="Achievements unlocked by the user"
    )
    
    # Timestamps
    last_action_at: Optional[datetime] = Field(
        default=None,
        description="When the last karma action was performed"
    )
    last_level_up_at: Optional[datetime] = Field(
        default=None,
        description="When the user last leveled up"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the summary was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the summary was last updated"
    )

    @classmethod
    def example(cls) -> 'KarmaSummary':
        """Create an example KarmaSummary instance"""
        now = datetime.now(UTC)
        return cls(
            user=UserReference(
                user_id="user_123",
                username="example_user",
                display_name="Example User"
            ),
            total_points=1250.5,
            current_level=3,
            level_progress=75.5,
            total_actions=42,
            positive_actions=38,
            negative_actions=4,
            action_breakdown={
                "report_creation": 15,
                "report_endorsement": 20,
                "report_resolution": 5,
                "report_comment": 2
            },
            current_streak=7,
            longest_streak=12,
            achievements={
                "first_report": True,
                "community_contributor": True,
                "problem_solver": True,
                "streak_master": False
            },
            last_action_at=now - timedelta(hours=2),
            last_level_up_at=now - timedelta(days=5),
            created_at=now - timedelta(days=30),
            updated_at=now
        )

class KarmaSummaryUpdate(BaseModel):
    """Model for updating karma summary"""
    total_points: Optional[float] = None
    current_level: Optional[int] = None
    level_progress: Optional[float] = None
    total_actions: Optional[int] = None
    positive_actions: Optional[int] = None
    negative_actions: Optional[int] = None
    action_breakdown: Optional[Dict[str, int]] = None
    current_streak: Optional[int] = None
    longest_streak: Optional[int] = None
    achievements: Optional[Dict[str, bool]] = None
    last_action_at: Optional[datetime] = None
    last_level_up_at: Optional[datetime] = None 