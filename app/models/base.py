from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid

def generate_uuid():
    """Generate a unique identifier."""
    return str(uuid.uuid4())

class BaseDBModel(BaseModel):
    """Base model with common fields for all documents."""
    
    # Unique identifier for each document
    id: str = Field(default_factory=generate_uuid, alias="_id")
    
    # Timestamps for document creation and updates
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        # Allow both id and _id to be used (MongoDB uses _id)
        allow_population_by_field_name = True
        # Preserve field aliases when converting to dict/json
        populate_by_name = True 