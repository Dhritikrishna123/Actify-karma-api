# KarmaCash data operations

from typing import Optional, List
from datetime import datetime, UTC
from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...models.karma_cash import KarmaCashTransaction, KarmaCashTransactionCreate
from ...models.karma_action import KarmaActionType
from ...models.user import UserReference
from ..mongodb import mongodb

class KarmaCashRepository:
    """Repository for karma cash-related database operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase = None):
        """Initialize repository with database connection."""
        self.db = db if db is not None else mongodb.get_db()
        self.collection = self.db.karma_cash_transactions
        
    async def create_transaction(self, transaction: KarmaCashTransactionCreate) -> KarmaCashTransaction:
        """Create a new karma cash transaction."""
        # Convert to dict and add timestamps
        transaction_dict = transaction.model_dump()
        transaction_dict["created_at"] = datetime.now(UTC)
        transaction_dict["updated_at"] = datetime.now(UTC)
        
        # Insert into database
        result = await self.collection.insert_one(transaction_dict)
        
        # Add ID and return as KarmaCashTransaction
        transaction_dict["_id"] = result.inserted_id
        return KarmaCashTransaction(**transaction_dict)
        
    async def get_user_balance(
        self,
        user_id: str
    ) -> float:
        """Get current karma cash balance for a user."""
        # Aggregate balance
        pipeline = [
            {"$match": {"user.id": user_id}},
            {"$group": {
                "_id": None,
                "balance": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$transaction_type", "CREDIT"]},
                            "$amount",
                            {"$multiply": ["$amount", -1]}
                        ]
                    }
                }
            }}
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        return result[0]["balance"] if result else 0.0
        
    async def get_user_transactions(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        transaction_type: Optional[str] = None
    ) -> List[KarmaCashTransaction]:
        """Get all karma cash transactions for a user."""
        # Build query
        query = {"user.id": user_id}
        if start_date or end_date:
            query["created_at"] = {}
            if start_date:
                query["created_at"]["$gte"] = start_date
            if end_date:
                query["created_at"]["$lte"] = end_date
        if transaction_type:
            query["transaction_type"] = transaction_type
            
        # Get transactions
        cursor = self.collection.find(query).sort("created_at", -1)
        transactions = await cursor.to_list(length=None)
        
        return [KarmaCashTransaction(**t) for t in transactions]
        
    async def get_transactions_by_action(
        self,
        action_type: KarmaActionType,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[KarmaCashTransaction]:
        """Get all karma cash transactions for a specific action type."""
        # Build query
        query = {"action_type": action_type}
        if start_date or end_date:
            query["created_at"] = {}
            if start_date:
                query["created_at"]["$gte"] = start_date
            if end_date:
                query["created_at"]["$lte"] = end_date
                
        # Get transactions
        cursor = self.collection.find(query).sort("created_at", -1)
        transactions = await cursor.to_list(length=None)
        
        return [KarmaCashTransaction(**t) for t in transactions]
        
    async def get_daily_transactions(
        self,
        date: datetime
    ) -> List[KarmaCashTransaction]:
        """Get all karma cash transactions for a specific day."""
        # Get start and end of day
        start_of_day = datetime.combine(date.date(), datetime.min.time())
        end_of_day = datetime.combine(date.date(), datetime.max.time())
        
        # Build query
        query = {
            "created_at": {
                "$gte": start_of_day,
                "$lte": end_of_day
            }
        }
        
        # Get transactions
        cursor = self.collection.find(query).sort("created_at", -1)
        transactions = await cursor.to_list(length=None)
        
        return [KarmaCashTransaction(**t) for t in transactions]
        
    async def get_top_earners(
        self,
        limit: int = 10,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[dict]:
        """Get top users by karma cash earnings."""
        # Build match stage
        match = {"transaction_type": "CREDIT"}
        if start_date or end_date:
            match["created_at"] = {}
            if start_date:
                match["created_at"]["$gte"] = start_date
            if end_date:
                match["created_at"]["$lte"] = end_date
                
        # Aggregate earnings by user
        pipeline = [
            {"$match": match},
            {"$group": {
                "_id": "$user.id",
                "total_earnings": {"$sum": "$amount"},
                "user": {"$first": "$user"}
            }},
            {"$sort": {"total_earnings": -1}},
            {"$limit": limit}
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=None)
        return result
