from typing import Optional, Dict, List
from pydantic import BaseModel, Field, validator
from .base import BaseDBModel
from datetime import datetime

class UserReference(BaseModel):
    """
    Reference to a user in the core database.
    This model will be updated once the core database schema is finalized.
    """
    core_user_id: str = Field(..., description="ID from the core database")
    username: Optional[str] = None
    email: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "core_user_id": "user123",
                "username": "john_doe",
                "email": "john@example.com"
            }
        }

class KarmaBalance(BaseModel):
    """Breakdown of different karma types."""
    civic_karma: float = Field(default=0, description="Karma from civic activities")
    skill_karma: float = Field(default=0, description="Karma from skill sharing")
    community_karma: float = Field(default=0, description="Karma from community activities")
    global_karma: float = Field(default=0, description="Overall karma score")
    karmacash_balance: float = Field(default=0, description="Convertible karma points")

class UserKarmaProfile(BaseDBModel):
    """
    Karma-specific user profile that extends core user data.
    Stores only karma-related information.
    """
    core_user_id: str = Field(..., description="Reference to core database user ID")
    verification_level: int = Field(
        default=0,
        description="User verification level (0=new, 1=email, 2=phone, 3=ID)"
    )
    karma_balance: KarmaBalance = Field(default_factory=KarmaBalance)
    trust_score: float = Field(
        default=0,
        ge=0,  # greater than or equal to 0
        le=100,  # less than or equal to 100
        description="User trust score (0-100)"
    )
    total_actions: int = Field(default=0, description="Total number of actions taken")
    valid_actions: int = Field(default=0, description="Number of verified valid actions")
    active_days: int = Field(default=0, description="Number of days user was active")
    last_action_at: Optional[datetime] = None
    achievements: List[str] = Field(default_factory=list, description="List of achievement IDs")
    endorsements_received: int = Field(default=0, description="Number of endorsements received")

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        schema_extra = {
            "example": {
                "core_user_id": "user123",
                "verification_level": 2,
                "karma_balance": {
                    "civic_karma": 100.0,
                    "skill_karma": 50.0,
                    "community_karma": 75.0,
                    "global_karma": 225.0,
                    "karmacash_balance": 10.0
                },
                "trust_score": 85.5,
                "total_actions": 150,
                "valid_actions": 145,
                "active_days": 30,
                "last_action_at": "2023-01-01T12:00:00Z",
                "achievements": ["early_adopter", "top_contributor"],
                "endorsements_received": 25
            }
        } 