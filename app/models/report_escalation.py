from typing import Optional, List, Dict
from datetime import datetime, UTC
from pydantic import BaseModel, Field, Any 
from enum import Enum

from .base import BaseDBModel
from .user import UserReference

class EscalationStatus(str, Enum):
    """Status of an escalation"""
    PENDING = "pending"  # Waiting for authority response
    RESPONDED = "responded"  # Authority has responded
    RESOLVED = "resolved"  # Issue has been resolved
    ESCALATED = "escalated"  # Escalated to higher authority
    REJECTED = "rejected"  # Escalation was rejected

class EscalationLevel(str, Enum):
    """Level of authority handling the escalation"""
    GRAM_PANCHAYAT = "gram_panchayat"
    BLOCK = "block"
    DISTRICT = "district"
    STATE = "state"
    CENTRAL = "central"

class EscalationResponse(BaseModel):
    """Response from an authority"""
    authority_id: str = Field(..., description="ID of the responding authority")
    response: str = Field(..., description="Authority's response")
    action_taken: Optional[str] = Field(None, description="Action taken by authority")
    next_steps: Optional[str] = Field(None, description="Planned next steps")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the response was made"
    )

class ReportEscalation(BaseDBModel):
    """Model for tracking report escalations"""
    # Report Information
    report_id: str = Field(..., description="ID of the report being escalated")
    
    # Current Authority
    current_authority_id: str = Field(..., description="ID of current handling authority")
    current_level: EscalationLevel = Field(..., description="Current authority level")
    
    # Escalation Details
    status: EscalationStatus = Field(
        default=EscalationStatus.PENDING,
        description="Current status of the escalation"
    )
    expected_response_time: datetime = Field(
        ...,
        description="Expected response time based on conditions"
    )
    actual_response_time: Optional[datetime] = Field(
        None,
        description="When the authority actually responded"
    )
    
    # Response Tracking
    responses: List[EscalationResponse] = Field(
        default_factory=list,
        description="History of authority responses"
    )
    
    # Escalation History
    escalation_path: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Path of authorities this report has been escalated through"
    )
    
    # Metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional escalation metadata"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the escalation was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the escalation was last updated"
    )

class ReportEscalationCreate(BaseModel):
    """Model for creating a new report escalation"""
    report_id: str
    current_authority_id: str
    current_level: EscalationLevel
    expected_response_time: datetime
    metadata: Optional[Dict[str, Any]] = None

class ReportEscalationUpdate(BaseModel):
    """Model for updating an existing report escalation"""
    status: Optional[EscalationStatus] = None
    response: Optional[EscalationResponse] = None
    metadata: Optional[Dict[str, Any]] = None 