from typing import List, Optional, Dict, Any
from datetime import datetime, UTC
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum
from .base import BaseDBModel
from .user import UserReference

class ReportStatus(str, Enum):
    """Status of a report in the system"""
    STAGING = "staging"  # Initial submission
    PROCESSING = "processing"  # Checking for duplicates
    VERIFIED = "verified"  # Unique report
    DUPLICATE = "duplicate"  # Matches existing report
    RESOLVED = "resolved"  # Issue has been fixed
    INVALID = "invalid"  # Report doesn't meet criteria

class Location(BaseModel):
    """Geographic location of the reported issue"""
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    address: Optional[str] = Field(None, description="Human-readable address")
    accuracy: Optional[float] = Field(None, description="Location accuracy in meters")

    @validator('latitude')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v

class ReportImage(BaseModel):
    """Image associated with a report"""
    url: HttpUrl = Field(..., description="Google Drive URL of the image")
    caption: Optional[str] = Field(None, description="Optional caption for the image")
    uploaded_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the image was uploaded"
    )
    processed: bool = Field(
        default=False,
        description="Whether the image has been processed by ML API"
    )
    vector_id: Optional[str] = Field(
        None,
        description="Reference ID for the vector embedding in FAISS"
    )
    similarity_score: Optional[float] = Field(
        None,
        description="Similarity score if image matches existing reports"
    )

class Endorsement(BaseModel):
    """User endorsement of a report"""
    user: UserReference
    comment: Optional[str] = Field(None, description="Optional comment with endorsement")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the endorsement was made"
    )

class AuthorityComment(BaseModel):
    """Official response from authorities"""
    comment: str = Field(..., description="Official comment on the report")
    status_update: Optional[str] = Field(None, description="Status update from authorities")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the comment was made"
    )

class SimilarReport(BaseModel):
    """Reference to a similar report"""
    report_id: str = Field(..., description="ID of the similar report")
    similarity_score: float = Field(..., description="Overall similarity score (0-1)")
    location_score: float = Field(..., description="Location similarity score")
    image_score: Optional[float] = Field(None, description="Image similarity score")
    text_score: Optional[float] = Field(None, description="Text similarity score")

class Report(BaseDBModel):
    """Main report model for public issues"""
    # Reporter Information
    reporter: UserReference = Field(..., description="User who submitted the report")
    
    # Report Details
    title: str = Field(..., min_length=5, max_length=100, description="Brief title of the issue")
    description: str = Field(..., min_length=20, max_length=1000, description="Detailed description")
    category: str = Field(..., description="Category of the issue")
    severity: str = Field(..., description="Severity level of the issue")
    
    # Location
    location: Location = Field(..., description="Where the issue was reported")
    
    # Media
    images: List[ReportImage] = Field(default_factory=list, description="Images of the issue")
    
    # Status and Processing
    status: ReportStatus = Field(
        default=ReportStatus.STAGING,
        description="Current status of the report"
    )
    processing_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata about the processing of this report"
    )
    similar_reports: List[SimilarReport] = Field(
        default_factory=list,
        description="References to similar reports"
    )
    
    # Community Interaction
    endorsements: List[Endorsement] = Field(
        default_factory=list,
        description="User endorsements of this report"
    )
    authority_comments: List[AuthorityComment] = Field(
        default_factory=list,
        description="Official responses from authorities"
    )
    
    # Karma and Tracking
    karma_awarded: bool = Field(
        default=False,
        description="Whether karma points have been awarded"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the report was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the report was last updated"
    )

class ReportCreate(BaseModel):
    """Model for creating a new report"""
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=20, max_length=1000)
    category: str
    severity: str
    location: Location
    images: List[HttpUrl] = Field(default_factory=list)

class ReportUpdate(BaseModel):
    """Model for updating an existing report"""
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=20, max_length=1000)
    category: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[ReportStatus] = None 