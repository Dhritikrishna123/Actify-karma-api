from typing import Optional, Dict, Any
from datetime import datetime, UTC
from pydantic import BaseModel, Field

from .base import BaseDBModel
from .karma_action import KarmaActionType

class KarmaRule(BaseDBModel):
    """Model for defining karma point rules"""
    # Rule Information
    action_type: KarmaActionType = Field(
        ...,
        description="Type of action this rule applies to"
    )
    points: float = Field(
        ...,
        description="Karma points to award/deduct (can be negative)"
    )
    description: str = Field(
        ...,
        description="Description of the rule"
    )
    
    # Conditions
    conditions: Dict[str, Any] = Field(
        default_factory=dict,
        description="Conditions that must be met for this rule to apply"
    )
    
    # Status
    is_active: bool = Field(
        default=True,
        description="Whether this rule is currently active"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the rule was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the rule was last updated"
    )

class KarmaRuleCreate(BaseModel):
    """Model for creating a new karma rule"""
    action_type: KarmaActionType
    points: float
    description: str
    conditions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = True

class KarmaRuleUpdate(BaseModel):
    """Model for updating an existing karma rule"""
    points: Optional[float] = None
    description: Optional[str] = None
    conditions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None 