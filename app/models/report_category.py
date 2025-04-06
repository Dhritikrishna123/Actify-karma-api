from typing import Optional, List, Dict
from datetime import datetime, UTC
from pydantic import BaseModel, Field
from enum import Enum

from .base import BaseDBModel

class CategoryPriority(str, Enum):
    """Priority levels for categories"""
    CRITICAL = "critical"    # Immediate attention required
    HIGH = "high"           # High priority
    MEDIUM = "medium"       # Normal priority
    LOW = "low"            # Low priority

class CategoryStatus(str, Enum):
    """Status of a category"""
    ACTIVE = "active"      # Category is active
    INACTIVE = "inactive"  # Category is inactive
    DEPRECATED = "deprecated"  # Category is no longer used

class CategoryMetadata(BaseModel):
    """Metadata for a category"""
    default_priority: CategoryPriority = Field(
        default=CategoryPriority.MEDIUM,
        description="Default priority for reports in this category"
    )
    response_time_weight: float = Field(
        default=1.0,
        description="Weight affecting response time calculation"
    )
    karma_multiplier: float = Field(
        default=1.0,
        description="Multiplier for karma points in this category"
    )
    required_fields: List[str] = Field(
        default_factory=list,
        description="Required fields for reports in this category"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Tags associated with this category"
    )

class ReportCategory(BaseDBModel):
    """Model for report categories"""
    # Basic Information
    name: str = Field(..., description="Name of the category")
    description: str = Field(..., description="Description of the category")
    parent_id: Optional[str] = Field(
        None,
        description="ID of parent category if this is a subcategory"
    )
    
    # Category Details
    status: CategoryStatus = Field(
        default=CategoryStatus.ACTIVE,
        description="Current status of the category"
    )
    metadata: CategoryMetadata = Field(
        default_factory=CategoryMetadata,
        description="Category metadata and configuration"
    )
    
    # Statistics
    report_count: int = Field(
        default=0,
        description="Number of reports in this category"
    )
    average_resolution_time: Optional[float] = Field(
        None,
        description="Average time to resolve reports in this category (in days)"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the category was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the category was last updated"
    )

class ReportCategoryCreate(BaseModel):
    """Model for creating a new report category"""
    name: str
    description: str
    parent_id: Optional[str] = None
    metadata: Optional[CategoryMetadata] = None

class ReportCategoryUpdate(BaseModel):
    """Model for updating an existing report category"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CategoryStatus] = None
    metadata: Optional[CategoryMetadata] = None 