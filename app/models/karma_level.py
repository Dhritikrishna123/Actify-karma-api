from typing import Optional, Dict, List
from datetime import datetime, UTC
from pydantic import BaseModel, Field

from .base import BaseDBModel

class LevelReward(BaseModel):
    """Model for level-specific rewards"""
    reward_type: str = Field(
        ...,
        description="Type of reward (e.g., 'badge', 'title', 'permission')"
    )
    reward_value: str = Field(
        ...,
        description="Value of the reward (e.g., badge name, permission name)"
    )
    description: str = Field(
        ...,
        description="Description of the reward"
    )

class KarmaLevel(BaseDBModel):
    """Model for defining karma levels and their requirements"""
    # Level Information
    level_number: int = Field(
        ...,
        description="Level number (1-based)"
    )
    level_name: str = Field(
        ...,
        description="Name of the level"
    )
    description: str = Field(
        ...,
        description="Description of the level"
    )
    
    # Requirements
    points_required: float = Field(
        ...,
        description="Karma points required to reach this level"
    )
    actions_required: Optional[int] = Field(
        default=None,
        description="Minimum number of actions required"
    )
    streak_required: Optional[int] = Field(
        default=None,
        description="Minimum streak required"
    )
    
    # Rewards
    rewards: List[LevelReward] = Field(
        default_factory=list,
        description="Rewards granted at this level"
    )
    
    # Status
    is_active: bool = Field(
        default=True,
        description="Whether this level is currently active"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the level was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the level was last updated"
    )

    @classmethod
    def example(cls) -> 'KarmaLevel':
        """Create an example KarmaLevel instance"""
        return cls(
            level_number=3,
            level_name="Community Contributor",
            description="Active member who regularly contributes to the community",
            points_required=1000.0,
            actions_required=30,
            streak_required=5,
            rewards=[
                LevelReward(
                    reward_type="badge",
                    reward_value="community_contributor",
                    description="Community Contributor Badge"
                ),
                LevelReward(
                    reward_type="permission",
                    reward_value="can_verify_reports",
                    description="Ability to verify reports"
                )
            ],
            is_active=True
        )

class KarmaLevelCreate(BaseModel):
    """Model for creating a new karma level"""
    level_number: int
    level_name: str
    description: str
    points_required: float
    actions_required: Optional[int] = None
    streak_required: Optional[int] = None
    rewards: Optional[List[LevelReward]] = None
    is_active: Optional[bool] = True

class KarmaLevelUpdate(BaseModel):
    """Model for updating an existing karma level"""
    level_name: Optional[str] = None
    description: Optional[str] = None
    points_required: Optional[float] = None
    actions_required: Optional[int] = None
    streak_required: Optional[int] = None
    rewards: Optional[List[LevelReward]] = None
    is_active: Optional[bool] = None 