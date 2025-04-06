# Trust models

from typing import Dict
from datetime import datetime
from pydantic import BaseModel, Field

from .user import UserReference

class TrustMetric(BaseModel):
    """Model for individual trust metrics."""
    name: str = Field(..., description="Name of the trust metric")
    value: float = Field(..., description="Value of the trust metric")
    weight: float = Field(1.0, description="Weight of the metric in overall score")

class TrustScoreCreate(BaseModel):
    """Model for creating a new trust score."""
    user: UserReference = Field(..., description="User reference")
    overall_score: float = Field(..., description="Overall trust score")
    metrics: Dict[str, float] = Field(..., description="Individual trust metrics")

class TrustScore(TrustScoreCreate):
    """Model for trust score with additional fields."""
    id: str = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp") 