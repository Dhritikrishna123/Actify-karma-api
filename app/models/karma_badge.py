from typing import Optional, Dict, List
from datetime import datetime, UTC
from pydantic import BaseModel, Field

from .base import BaseDBModel

class BadgeRequirement(BaseModel):
    """Model for badge requirements"""
    requirement_type: str = Field(
        ...,
        description="Type of requirement (e.g., 'level', 'achievement', 'points')"
    )
    requirement_value: str = Field(
        ...,
        description="Value required to earn the badge"
    )
    description: str = Field(
        ...,
        description="Description of the requirement"
    )

class KarmaBadge(BaseDBModel):
    """Model for defining karma badges"""
    # Badge Information
    badge_id: str = Field(
        ...,
        description="Unique identifier for the badge"
    )
    name: str = Field(
        ...,
        description="Name of the badge"
    )
    description: str = Field(
        ...,
        description="Description of the badge"
    )
    category: str = Field(
        ...,
        description="Category of the badge (e.g., 'reporting', 'community', 'authority')"
    )
    
    # Visual Information
    icon_url: str = Field(
        ...,
        description="URL to the badge icon"
    )
    rarity: str = Field(
        default="common",
        description="Rarity level of the badge (common, rare, epic, legendary)"
    )
    
    # Requirements
    requirements: List[BadgeRequirement] = Field(
        default_factory=list,
        description="Requirements to earn this badge"
    )
    
    # Effects
    effects: Dict[str, str] = Field(
        default_factory=dict,
        description="Special effects or benefits of the badge"
    )
    
    # Status
    is_active: bool = Field(
        default=True,
        description="Whether this badge is currently active"
    )
    is_hidden: bool = Field(
        default=False,
        description="Whether this badge is hidden until earned"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the badge was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the badge was last updated"
    )

    @classmethod
    def example(cls) -> 'KarmaBadge':
        """Create an example KarmaBadge instance"""
        return cls(
            badge_id="community_hero",
            name="Community Hero",
            description="Awarded for exceptional community contributions",
            category="community",
            icon_url="https://example.com/badges/community_hero.png",
            rarity="epic",
            requirements=[
                BadgeRequirement(
                    requirement_type="level",
                    requirement_value="5",
                    description="Reach level 5"
                ),
                BadgeRequirement(
                    requirement_type="achievement",
                    requirement_value="community_contributor",
                    description="Earn Community Contributor achievement"
                )
            ],
            effects={
                "profile_highlight": "true",
                "special_icon": "true"
            },
            is_active=True,
            is_hidden=False
        )

class KarmaBadgeCreate(BaseModel):
    """Model for creating a new karma badge"""
    badge_id: str
    name: str
    description: str
    category: str
    icon_url: str
    rarity: Optional[str] = "common"
    requirements: Optional[List[BadgeRequirement]] = None
    effects: Optional[Dict[str, str]] = None
    is_active: Optional[bool] = True
    is_hidden: Optional[bool] = False

class KarmaBadgeUpdate(BaseModel):
    """Model for updating an existing karma badge"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    icon_url: Optional[str] = None
    rarity: Optional[str] = None
    requirements: Optional[List[BadgeRequirement]] = None
    effects: Optional[Dict[str, str]] = None
    is_active: Optional[bool] = None
    is_hidden: Optional[bool] = None 