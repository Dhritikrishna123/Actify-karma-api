from typing import Optional, List, Dict, Any
from datetime import datetime, UTC
from pydantic import BaseModel, Field, EmailStr, HttpUrl, validator, Any 
from enum import Enum

from .base import BaseDBModel
from .user import UserReference

class AuthorityType(str, Enum):
    """Types of authorities in the system"""
    GRAM_PANCHAYAT = "gram_panchayat"  # Village level
    BLOCK = "block"  # Block level
    DISTRICT = "district"  # District level
    STATE = "state"  # State level
    CENTRAL = "central"  # Central government
    NGO = "ngo"  # Non-Governmental Organization
    PRIVATE = "private"  # Private organizations
    COMMUNITY = "community"  # Community organizations

class AuthorityStatus(str, Enum):
    """Status of an authority account"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"

class AuthorityContact(BaseModel):
    """Contact information for an authority"""
    name: str = Field(..., description="Contact person's name")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone number")
    designation: Optional[str] = Field(None, description="Contact's designation/role")

class AuthorityHierarchy(BaseModel):
    """Hierarchy information for an authority"""
    parent_id: Optional[str] = Field(None, description="ID of parent authority")
    child_ids: List[str] = Field(
        default_factory=list,
        description="IDs of child authorities"
    )
    level: int = Field(
        ...,
        description="Hierarchy level (1=Gram Panchayat, 2=Block, 3=District, 4=State, 5=Central)"
    )

class AuthorityJurisdiction(BaseModel):
    """Geographic jurisdiction of an authority"""
    gram_panchayat: Optional[str] = Field(None, description="Gram Panchayat name")
    block: Optional[str] = Field(None, description="Block name")
    district: str = Field(..., description="District name")
    state: str = Field(..., description="State name")
    country: str = Field(default="India", description="Country name")
    pincode: Optional[str] = Field(None, description="PIN code")
    coordinates: Optional[List[float]] = Field(None, description="[longitude, latitude] of jurisdiction center")

class EscalationCondition(BaseModel):
    """Conditions that affect response time and escalation"""
    category_weights: Dict[str, float] = Field(
        default_factory=lambda: {
            "infrastructure": 1.0,
            "health": 0.8,
            "education": 0.9,
            "environment": 0.7,
            "safety": 0.6
        },
        description="Weight multipliers for different report categories"
    )
    urgency_weights: Dict[str, float] = Field(
        default_factory=lambda: {
            "critical": 0.5,    # 50% of base time
            "high": 0.7,        # 70% of base time
            "medium": 1.0,      # 100% of base time
            "low": 1.5          # 150% of base time
        },
        description="Weight multipliers for different urgency levels"
    )
    endorsement_thresholds: Dict[int, float] = Field(
        default_factory=lambda: {
            10: 0.8,    # 20% reduction for 10+ endorsements
            25: 0.6,    # 40% reduction for 25+ endorsements
            50: 0.4,    # 60% reduction for 50+ endorsements
            100: 0.2    # 80% reduction for 100+ endorsements
        },
        description="Endorsement count thresholds and their time reduction factors"
    )
    base_response_time: int = Field(
        default=7,
        description="Base response time in days"
    )

class AuthorityEscalation(BaseModel):
    """Escalation rules for reports"""
    conditions: EscalationCondition = Field(
        default_factory=EscalationCondition,
        description="Conditions affecting response time"
    )
    auto_escalate: bool = Field(
        default=True,
        description="Whether to automatically escalate unresolved reports"
    )
    escalation_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of escalations for this authority"
    )
    performance_metrics: Dict[str, float] = Field(
        default_factory=lambda: {
            "average_response_time": 0.0,
            "escalation_rate": 0.0,
            "resolution_rate": 0.0
        },
        description="Authority's performance metrics"
    )

    def calculate_response_time(
        self,
        category: str,
        urgency: str,
        endorsement_count: int
    ) -> int:
        """Calculate dynamic response time based on report characteristics"""
        # Get base weights
        category_weight = self.conditions.category_weights.get(category, 1.0)
        urgency_weight = self.conditions.urgency_weights.get(urgency, 1.0)
        
        # Calculate endorsement reduction
        endorsement_reduction = 1.0
        for threshold, reduction in sorted(
            self.conditions.endorsement_thresholds.items(),
            reverse=True
        ):
            if endorsement_count >= threshold:
                endorsement_reduction = reduction
                break
        
        # Calculate final response time
        base_time = self.conditions.base_response_time
        final_time = base_time * category_weight * urgency_weight * endorsement_reduction
        
        # Ensure minimum response time of 1 day
        return max(1, int(final_time))

class Authority(BaseDBModel):
    """Model for official authorities in the system"""
    # Basic Information
    name: str = Field(..., description="Name of the authority")
    type: AuthorityType = Field(..., description="Type of authority")
    status: AuthorityStatus = Field(
        default=AuthorityStatus.PENDING,
        description="Current status of the authority account"
    )
    
    # Hierarchy Information
    hierarchy: AuthorityHierarchy = Field(
        ...,
        description="Authority hierarchy information"
    )
    
    # Contact Information
    contacts: List[AuthorityContact] = Field(
        default_factory=list,
        description="List of contact persons"
    )
    website: Optional[HttpUrl] = Field(None, description="Official website")
    office_address: Optional[str] = Field(None, description="Physical office address")
    
    # Jurisdiction
    jurisdiction: AuthorityJurisdiction = Field(
        ...,
        description="Geographic jurisdiction details"
    )
    
    # Escalation Rules
    escalation: AuthorityEscalation = Field(
        default_factory=AuthorityEscalation,
        description="Report escalation rules"
    )
    
    # Authentication
    admin_user: UserReference = Field(
        ...,
        description="Primary admin user for this authority"
    )
    authorized_users: List[UserReference] = Field(
        default_factory=list,
        description="List of authorized users"
    )
    
    # Metadata
    metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Additional authority metadata"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the authority was registered"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the authority was last updated"
    )

    @validator('hierarchy')
    def validate_hierarchy(cls, v, values):
        """Validate hierarchy level based on authority type"""
        type_to_level = {
            AuthorityType.GRAM_PANCHAYAT: 1,
            AuthorityType.BLOCK: 2,
            AuthorityType.DISTRICT: 3,
            AuthorityType.STATE: 4,
            AuthorityType.CENTRAL: 5,
            AuthorityType.NGO: 0,
            AuthorityType.PRIVATE: 0,
            AuthorityType.COMMUNITY: 0
        }
        
        if 'type' in values:
            expected_level = type_to_level[values['type']]
            if v.level != expected_level and expected_level != 0:
                raise ValueError(f"Invalid hierarchy level for authority type {values['type']}")
        return v

class AuthorityCreate(BaseModel):
    """Model for creating a new authority"""
    name: str
    type: AuthorityType
    hierarchy: AuthorityHierarchy
    contacts: List[AuthorityContact]
    jurisdiction: AuthorityJurisdiction
    admin_user: UserReference
    website: Optional[HttpUrl] = None
    office_address: Optional[str] = None
    escalation: Optional[AuthorityEscalation] = None
    metadata: Optional[Dict[str, str]] = None

class AuthorityUpdate(BaseModel):
    """Model for updating an existing authority"""
    name: Optional[str] = None
    status: Optional[AuthorityStatus] = None
    contacts: Optional[List[AuthorityContact]] = None
    website: Optional[HttpUrl] = None
    office_address: Optional[str] = None
    jurisdiction: Optional[AuthorityJurisdiction] = None
    escalation: Optional[AuthorityEscalation] = None
    metadata: Optional[Dict[str, str]] = None 