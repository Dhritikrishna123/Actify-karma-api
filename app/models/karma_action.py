from typing import Optional
from datetime import datetime, UTC
from enum import Enum
from pydantic import BaseModel, Field

from .base import BaseDBModel

class KarmaActionType(str, Enum):
    """Enum defining all possible karma action types"""
    # Content Actions
    CONTENT_CREATION = "content_creation"
    CONTENT_UPDATE = "content_update"
    CONTENT_DELETION = "content_deletion"
    CONTENT_SHARE = "content_share"
    CONTENT_COMMENT = "content_comment"
    CONTENT_LIKE = "content_like"
    
    # Community Actions
    COMMUNITY_HELP = "community_help"
    COMMUNITY_MODERATION = "community_moderation"
    COMMUNITY_GUIDANCE = "community_guidance"
    COMMUNITY_EVENT = "community_event"
    
    # Verification Actions
    VERIFICATION = "verification"
    IDENTITY_VERIFICATION = "identity_verification"
    EXPERTISE_VERIFICATION = "expertise_verification"
    AFFILIATION_VERIFICATION = "affiliation_verification"
    
    # Report Actions
    REPORT_CREATION = "report_creation"
    REPORT_ENDORSEMENT = "report_endorsement"
    REPORT_RESOLUTION = "report_resolution"
    REPORT_ESCALATION = "report_escalation"
    AUTHORITY_RESPONSE = "authority_response"
    REPORT_UPDATE = "report_update"
    REPORT_COMMENT = "report_comment"
    REPORT_SHARE = "report_share"
    REPORT_VERIFICATION = "report_verification"
    REPORT_FLAG = "report_flag"
    
    # Authority Actions
    AUTHORITY_VERIFICATION = "authority_verification"
    AUTHORITY_ESCALATION = "authority_escalation"
    AUTHORITY_RESOLUTION = "authority_resolution"
    AUTHORITY_UPDATE = "authority_update"
    AUTHORITY_COMMENT = "authority_comment"
    AUTHORITY_SHARE = "authority_share"
    AUTHORITY_FLAG = "authority_flag"
    
    # User Actions
    USER_VERIFICATION = "user_verification"
    USER_ESCALATION = "user_escalation"
    USER_RESOLUTION = "user_resolution"
    USER_UPDATE = "user_update"
    USER_COMMENT = "user_comment"
    USER_SHARE = "user_share"
    USER_FLAG = "user_flag"

class KarmaActionMetadata(BaseModel):
    """Model for action-specific metadata"""
    base_points: float = Field(
        default=0.0,
        description="Base points awarded for this action"
    )
    max_points: Optional[float] = Field(
        default=None,
        description="Maximum points that can be awarded"
    )
    min_points: Optional[float] = Field(
        default=None,
        description="Minimum points that can be awarded"
    )
    cooldown_period: Optional[int] = Field(
        default=None,
        description="Cooldown period in seconds between actions"
    )
    daily_limit: Optional[int] = Field(
        default=None,
        description="Maximum number of times this action can be performed per day"
    )
    multiplier: Optional[float] = Field(
        default=1.0,
        description="Multiplier for points calculation"
    )

class KarmaAction(BaseDBModel):
    """Model for defining karma action types and their behavior"""
    # Action Information
    action_type: KarmaActionType = Field(
        ...,
        description="Type of action"
    )
    name: str = Field(
        ...,
        description="Display name of the action"
    )
    description: str = Field(
        ...,
        description="Description of the action"
    )
    metadata: KarmaActionMetadata = Field(
        default_factory=KarmaActionMetadata,
        description="Action-specific metadata"
    )
    
    # Status
    is_active: bool = Field(
        default=True,
        description="Whether this action type is currently active"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the action type was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the action type was last updated"
    )

class KarmaActionCreate(BaseModel):
    """Model for creating a new karma action"""
    action_type: KarmaActionType
    name: str
    description: str
    metadata: Optional[KarmaActionMetadata] = None
    is_active: Optional[bool] = True

class KarmaActionUpdate(BaseModel):
    """Model for updating an existing karma action"""
    name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[KarmaActionMetadata] = None
    is_active: Optional[bool] = None 