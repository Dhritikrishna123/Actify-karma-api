# Karma operation routes

from typing import Optional, List, Dict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field

from .....db.repositories.karma_repository import KarmaRepository
from .....models.karma import KarmaTransaction, KarmaTransactionCreate
from .....models.user import UserReference

router = APIRouter(tags=["karma_scores"])

class KarmaResponse(BaseModel):
    """Response model for karma operations."""
    overall_score: float = Field(..., description="Overall karma score")
    domain_scores: Dict[str, float] = Field(..., description="Karma scores by domain")
    history: List[KarmaTransaction] = Field(..., description="Karma transaction history")

# Import the dependency function after router creation
from ..karma_router import get_karma_repository

@router.post("/transactions", response_model=KarmaTransaction)
async def create_karma_transaction(
    transaction: KarmaTransactionCreate,
    karma_repository: KarmaRepository = Depends(get_karma_repository)
):
    """Create a new karma transaction."""
    try:
        return await karma_repository.create_transaction(transaction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}", response_model=KarmaResponse)
async def get_user_karma(
    user_id: str = Path(..., description="The ID of the user"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    karma_repository: KarmaRepository = Depends(get_karma_repository)
):
    """Get user's karma score and history."""
    try:
        current_score = await karma_repository.get_user_karma_score(user_id)
        if not current_score:
            raise HTTPException(status_code=404, detail="Karma score not found")
            
        history = await karma_repository.get_user_karma_history(user_id, start_date, end_date)
        
        return KarmaResponse(
            overall_score=current_score.overall_score,
            domain_scores=current_score.domain_scores,
            history=history
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}/domains/{domain}", response_model=KarmaResponse)
async def get_user_domain_karma(
    user_id: str = Path(..., description="The ID of the user"),
    domain: str = Path(..., description="The karma domain to query"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    karma_repository: KarmaRepository = Depends(get_karma_repository)
):
    """Get user's karma score for a specific domain."""
    try:
        current_score = await karma_repository.get_user_domain_karma(user_id, domain)
        if not current_score:
            raise HTTPException(status_code=404, detail="Domain karma score not found")
            
        history = await karma_repository.get_user_domain_history(user_id, domain, start_date, end_date)
        
        return KarmaResponse(
            overall_score=current_score,
            domain_scores={domain: current_score},
            history=history
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-users", response_model=List[dict])
async def get_top_karma_users(
    limit: int = 10,
    domain: Optional[str] = None,
    karma_repository: KarmaRepository = Depends(get_karma_repository)
):
    """Get list of top karma users."""
    try:
        return await karma_repository.get_top_karma_users(limit, domain)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 