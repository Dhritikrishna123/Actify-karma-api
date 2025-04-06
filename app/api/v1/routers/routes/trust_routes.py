# Trust score operation routes

from typing import Optional, List, Dict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel, Field

from .....db.repositories.trust_repository import TrustRepository
from .....models.trust import TrustScore, TrustMetric
from .....models.user import UserReference

router = APIRouter(prefix="/trust", tags=["trust_scores"])

class TrustResponse(BaseModel):
    """Response model for trust operations."""
    overall_score: float = Field(..., description="Overall trust score")
    metrics: Dict[str, float] = Field(..., description="Individual trust metrics")
    history: List[TrustScore] = Field(..., description="Trust score history")

# Import the dependency function after router creation
from ..karma_router import get_trust_repository

@router.get("/user/{user_id}", response_model=TrustResponse)
async def get_user_trust(
    user_id: str = Path(..., description="The ID of the user"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    trust_repository: TrustRepository = Depends(get_trust_repository)
):
    """Get user's trust score and history."""
    try:
        current_score = await trust_repository.get_user_trust_score(user_id)
        if not current_score:
            raise HTTPException(status_code=404, detail="Trust score not found")
            
        history = await trust_repository.get_user_trust_history(user_id, start_date, end_date)
        
        return TrustResponse(
            overall_score=current_score.overall_score,
            metrics=current_score.metrics,
            history=history
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/user/{user_id}/metric/{metric_name}")
async def update_trust_metric(
    user_id: str = Path(..., description="The ID of the user"),
    metric_name: str = Path(..., description="The name of the metric to update"),
    value: float = Query(..., ge=0.0, le=1.0, description="The new value for the metric"),
    trust_repository: TrustRepository = Depends(get_trust_repository)
):
    """Update a specific trust metric for a user."""
    try:
        await trust_repository.update_trust_metric(user_id, metric_name, value)
        return {"message": "Trust metric updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-users", response_model=List[dict])
async def get_top_trusted_users(
    limit: int = 10,
    metric: Optional[str] = None,
    trust_repository: TrustRepository = Depends(get_trust_repository)
):
    """Get list of top trusted users."""
    try:
        return await trust_repository.get_top_trusted_users(limit, metric)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 