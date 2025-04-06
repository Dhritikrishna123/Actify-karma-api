from typing import Optional, Dict, List
from datetime import datetime, UTC
from pydantic import BaseModel, Field

from .base import BaseDBModel

class PermissionRequirement(BaseModel):
    """Model for permission requirements"""
    requirement_type: str = Field(
        ...,
        description="Type of requirement (e.g., 'level', 'achievement', 'points')"
    )
    requirement_value: str = Field(
        ...,
        description="Value required to earn the permission"
    )
    description: str = Field(
        ...,
        description="Description of the requirement"
    )

class PermissionEffect(BaseModel):
    """Model for permission effects"""
    effect_type: str = Field(
        ...,
        description="Type of effect (e.g., 'access', 'limit', 'override')"
    )
    effect_value: str = Field(
        ...,
        description="Value of the effect"
    )
    description: str = Field(
        ...,
        description="Description of the effect"
    )

class KarmaPermission(BaseDBModel):
    """Model for defining karma permissions"""
    # Permission Information
    permission_id: str = Field(
        ...,
        description="Unique identifier for the permission"
    )
    name: str = Field(
        ...,
        description="Name of the permission"
    )
    description: str = Field(
        ...,
        description="Description of the permission"
    )
    category: str = Field(
        ...,
        description="Category of the permission (e.g., 'reporting', 'moderation', 'administration')"
    )
    
    # Requirements
    requirements: List[PermissionRequirement] = Field(
        default_factory=list,
        description="Requirements to earn this permission"
    )
    
    # Effects
    effects: List[PermissionEffect] = Field(
        default_factory=list,
        description="Effects and capabilities granted by this permission"
    )
    
    # Status
    is_active: bool = Field(
        default=True,
        description="Whether this permission is currently active"
    )
    is_hidden: bool = Field(
        default=False,
        description="Whether this permission is hidden until earned"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the permission was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the permission was last updated"
    )

    @classmethod
    def example(cls) -> 'KarmaPermission':
        """Create an example KarmaPermission instance"""
        return cls(
            permission_id="verify_reports",
            name="Report Verification",
            description="Ability to verify reports for accuracy",
            category="moderation",
            requirements=[
                PermissionRequirement(
                    requirement_type="level",
                    requirement_value="3",
                    description="Reach level 3"
                ),
                PermissionRequirement(
                    requirement_type="achievement",
                    requirement_value="trusted_verifier",
                    description="Earn Trusted Verifier achievement"
                )
            ],
            effects=[
                PermissionEffect(
                    effect_type="access",
                    effect_value="verify_reports",
                    description="Can verify reports"
                ),
                PermissionEffect(
                    effect_type="limit",
                    effect_value="daily_verifications:10",
                    description="Can verify up to 10 reports per day"
                )
            ],
            is_active=True,
            is_hidden=False
        )

class KarmaPermissionCreate(BaseModel):
    """Model for creating a new karma permission"""
    permission_id: str
    name: str
    description: str
    category: str
    requirements: Optional[List[PermissionRequirement]] = None
    effects: Optional[List[PermissionEffect]] = None
    is_active: Optional[bool] = True
    is_hidden: Optional[bool] = False

class KarmaPermissionUpdate(BaseModel):
    """Model for updating an existing karma permission"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    requirements: Optional[List[PermissionRequirement]] = None
    effects: Optional[List[PermissionEffect]] = None
    is_active: Optional[bool] = None
    is_hidden: Optional[bool] = None 