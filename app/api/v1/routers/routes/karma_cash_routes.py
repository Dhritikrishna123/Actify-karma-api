# Karma cash operation routes

from typing import Optional, List, Dict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field

from .....db.repositories.karma_cash_repository import KarmaCashRepository
from .....models.karma_cash import KarmaCashTransaction, KarmaCashTransactionCreate
from .....models.user import UserReference

router = APIRouter(prefix="/karma-cash", tags=["karma_cash"])

class KarmaCashResponse(BaseModel):
    """Response model for karma cash operations."""
    balance: float = Field(..., description="Current karma cash balance")
    transactions: List[KarmaCashTransaction] = Field(..., description="Transaction history")

# Import the dependency function after router creation
from ..karma_router import get_karma_cash_repository

@router.get("/user/{user_id}", response_model=KarmaCashResponse)
async def get_user_karma_cash(
    user_id: str = Path(..., description="The ID of the user"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    karma_cash_repository: KarmaCashRepository = Depends(get_karma_cash_repository)
):
    """Get user's karma cash balance and history."""
    try:
        balance = await karma_cash_repository.get_user_balance(user_id)
        transactions = await karma_cash_repository.get_user_transactions(user_id, start_date, end_date)
        
        return KarmaCashResponse(
            balance=balance,
            transactions=transactions
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/daily", response_model=List[KarmaCashTransaction])
async def get_daily_transactions(
    date: Optional[datetime] = None,
    karma_cash_repository: KarmaCashRepository = Depends(get_karma_cash_repository)
):
    """Get all karma cash transactions for a specific day."""
    try:
        # Use today's date if no date is provided
        if date is None:
            date = datetime.now()
        return await karma_cash_repository.get_daily_transactions(date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-earners", response_model=List[dict])
async def get_top_earners(
    limit: int = 10,
    karma_cash_repository: KarmaCashRepository = Depends(get_karma_cash_repository)
):
    """Get list of top karma cash earners."""
    try:
        return await karma_cash_repository.get_top_earners(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 