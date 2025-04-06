from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum
from bson import ObjectId

from .base import BaseDBModel
from .user import UserReference
from .karma_action import KarmaActionType

class KarmaTransaction(BaseDBModel):
    """Model for tracking individual karma transactions"""
    # Transaction Information
    user: UserReference = Field(
        ...,
        description="User who performed the action"
    )
    action_type: KarmaActionType = Field(
        ...,
        description="Type of action that triggered this transaction"
    )
    points: float = Field(
        ...,
        description="Karma points awarded/deducted (can be negative)"
    )
    
    # Context
    context_id: Optional[str] = Field(
        default=None,
        description="ID of the related entity (e.g., report_id, authority_id)"
    )
    context_type: Optional[str] = Field(
        default=None,
        description="Type of the related entity (e.g., 'report', 'authority')"
    )
    description: Optional[str] = Field(
        default=None,
        description="Additional description of the transaction"
    )
    
    # Status
    is_reversed: bool = Field(
        default=False,
        description="Whether this transaction has been reversed"
    )
    reversed_at: Optional[datetime] = Field(
        default=None,
        description="When the transaction was reversed"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the transaction was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the transaction was last updated"
    )

    @validator('id', pre=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        use_enum_values = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

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
        default_factory=datetime.utcnow,
        description="When the rule was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the rule was last updated"
    )

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        use_enum_values = True

class KarmaTransactionCreate(BaseModel):
    """Model for creating new karma transactions"""
    user: UserReference = Field(
        ...,
        description="User who performed the action"
    )
    action_type: KarmaActionType = Field(
        ...,
        description="Type of action that triggered this transaction"
    )
    points: float = Field(
        ...,
        description="Karma points awarded/deducted (can be negative)"
    )
    domain: str = Field(
        ...,
        description="Domain of the action (e.g., 'content', 'community')"
    )
    context_id: Optional[str] = Field(
        default=None,
        description="ID of the related entity"
    )
    context_type: Optional[str] = Field(
        default=None,
        description="Type of the related entity"
    )
    description: Optional[str] = Field(
        default=None,
        description="Additional description of the transaction"
    )

class KarmaRuleCreate(BaseModel):
    """Model for creating a new karma rule"""
    action_type: KarmaActionType
    points: float
    description: str
    conditions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = True

    class Config:
        use_enum_values = True

class KarmaRuleUpdate(BaseModel):
    """Model for updating an existing karma rule"""
    points: Optional[float] = None
    description: Optional[str] = None
    conditions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class KarmaTransactionUpdate(BaseModel):
    """Model for updating an existing karma transaction"""
    is_reversed: Optional[bool] = None
    description: Optional[str] = None

@validator('points')
def validate_points(cls, v):
    """Validate that points are not zero."""
    if v == 0:
        raise ValueError("Points cannot be zero")
    return v

class KarmaScore(BaseModel):
    """Model for representing a user's karma score"""
    overall_score: float = Field(
        default=0.0,
        description="Overall karma score across all domains"
    )
    domain_scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Karma scores by domain"
    ) 