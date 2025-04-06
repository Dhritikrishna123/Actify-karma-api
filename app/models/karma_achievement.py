from typing import Optional, Dict, List
from datetime import datetime, UTC
from pydantic import BaseModel, Field

from .base import BaseDBModel

class AchievementReward(BaseModel):
    """Model for achievement-specific rewards"""
    reward_type: str = Field(
        ...,
        description="Type of reward (e.g., 'badge', 'title', 'permission', 'points')"
    )
    reward_value: str = Field(
        ...,
        description="Value of the reward (e.g., badge name, permission name, point amount)"
    )
    description: str = Field(
        ...,
        description="Description of the reward"
    )

class AchievementRequirement(BaseModel):
    """Model for achievement requirements"""
    requirement_type: str = Field(
        ...,
        description="Type of requirement (e.g., 'points', 'actions', 'streak')"
    )
    requirement_value: float = Field(
        ...,
        description="Value required to complete the requirement"
    )
    description: str = Field(
        ...,
        description="Description of the requirement"
    )

class KarmaAchievement(BaseDBModel):
    """Model for defining karma achievements"""
    # Achievement Information
    achievement_id: str = Field(
        ...,
        description="Unique identifier for the achievement"
    )
    name: str = Field(
        ...,
        description="Name of the achievement"
    )
    description: str = Field(
        ...,
        description="Description of the achievement"
    )
    category: str = Field(
        ...,
        description="Category of the achievement (e.g., 'reporting', 'community', 'authority')"
    )
    
    # Requirements
    requirements: List[AchievementRequirement] = Field(
        ...,
        description="List of requirements to unlock this achievement"
    )
    
    # Rewards
    rewards: List[AchievementReward] = Field(
        default_factory=list,
        description="Rewards granted for completing this achievement"
    )
    
    # Status
    is_active: bool = Field(
        default=True,
        description="Whether this achievement is currently active"
    )
    is_hidden: bool = Field(
        default=False,
        description="Whether this achievement is hidden until unlocked"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the achievement was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the achievement was last updated"
    )

    @classmethod
    def example(cls) -> 'KarmaAchievement':
        """Create an example KarmaAchievement instance"""
        return cls(
            achievement_id="first_report",
            name="First Report",
            description="Create your first report on the platform",
            category="reporting",
            requirements=[
                AchievementRequirement(
                    requirement_type="actions",
                    requirement_value=1,
                    description="Create at least one report"
                )
            ],
            rewards=[
                AchievementReward(
                    reward_type="badge",
                    reward_value="first_report",
                    description="First Report Badge"
                ),
                AchievementReward(
                    reward_type="points",
                    reward_value="100",
                    description="100 Karma Points"
                )
            ],
            is_active=True,
            is_hidden=False
        )

class KarmaAchievementCreate(BaseModel):
    """Model for creating a new karma achievement"""
    achievement_id: str
    name: str
    description: str
    category: str
    requirements: List[AchievementRequirement]
    rewards: Optional[List[AchievementReward]] = None
    is_active: Optional[bool] = True
    is_hidden: Optional[bool] = False

class KarmaAchievementUpdate(BaseModel):
    """Model for updating an existing karma achievement"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    requirements: Optional[List[AchievementRequirement]] = None
    rewards: Optional[List[AchievementReward]] = None
    is_active: Optional[bool] = None
    is_hidden: Optional[bool] = None 