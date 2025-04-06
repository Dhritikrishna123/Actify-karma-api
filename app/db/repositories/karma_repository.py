# Karma data operations

from typing import Optional, List
from datetime import datetime, UTC
from bson import ObjectId
from pydantic import BaseModel

from ...models.karma import KarmaTransaction, KarmaTransactionCreate
from ...models.karma_action import KarmaActionType
from ...models.user import UserReference
from ..mongodb import mongodb

class KarmaRepository:
    """Repository for karma-related database operations."""
    
    def __init__(self):
        """Initialize repository with database connection."""
        self.db = mongodb.get_db()
        self.collection = self.db.karma_transactions
        
    async def create_transaction(self, transaction: KarmaTransactionCreate) -> KarmaTransaction:
        """Create a new karma transaction."""
        # Convert to dict and add timestamps
        transaction_dict = transaction.model_dump()
        transaction_dict["created_at"] = datetime.now(UTC)
        transaction_dict["updated_at"] = datetime.now(UTC)
        
        # Insert into database
        result = await self.collection.insert_one(transaction_dict)
        
        # Add ID and return as KarmaTransaction
        transaction_dict["_id"] = result.inserted_id
        return KarmaTransaction(**transaction_dict)
        
    async def get_user_karma(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> float:
        """Get total karma points for a user within a date range."""
        # Build query
        query = {"user.id": user_id}
        if start_date or end_date:
            query["created_at"] = {}
            if start_date:
                query["created_at"]["$gte"] = start_date
            if end_date:
                query["created_at"]["$lte"] = end_date
                
        # Aggregate points
        pipeline = [
            {"$match": query},
            {"$group": {"_id": None, "total": {"$sum": "$points"}}}
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0.0
        
    async def get_user_karma_by_domain(
        self,
        user_id: str,
        domain: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> float:
        """Get total karma points for a user in a specific domain."""
        # Build query
        query = {
            "user.id": user_id,
            "domain": domain
        }
        if start_date or end_date:
            query["created_at"] = {}
            if start_date:
                query["created_at"]["$gte"] = start_date
            if end_date:
                query["created_at"]["$lte"] = end_date
                
        # Aggregate points
        pipeline = [
            {"$match": query},
            {"$group": {"_id": None, "total": {"$sum": "$points"}}}
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0.0
        
    async def get_user_actions(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[KarmaTransaction]:
        """Get all karma actions for a user within a date range."""
        # Build query
        query = {"user.id": user_id}
        if start_date or end_date:
            query["created_at"] = {}
            if start_date:
                query["created_at"]["$gte"] = start_date
            if end_date:
                query["created_at"]["$lte"] = end_date
                
        # Get transactions
        cursor = self.collection.find(query).sort("created_at", -1)
        transactions = await cursor.to_list(length=None)
        
        return [KarmaTransaction(**t) for t in transactions]
        
    async def get_user_actions_by_domain(
        self,
        user_id: str,
        domain: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[KarmaTransaction]:
        """Get all karma actions for a user in a specific domain."""
        # Build query
        query = {
            "user.id": user_id,
            "domain": domain
        }
        if start_date or end_date:
            query["created_at"] = {}
            if start_date:
                query["created_at"]["$gte"] = start_date
            if end_date:
                query["created_at"]["$lte"] = end_date
                
        # Get transactions
        cursor = self.collection.find(query).sort("created_at", -1)
        transactions = await cursor.to_list(length=None)
        
        return [KarmaTransaction(**t) for t in transactions]
        
    async def get_user_actions_today(
        self,
        user_id: str,
        action_type: KarmaActionType,
        date: datetime
    ) -> List[KarmaTransaction]:
        """Get user's actions of a specific type for today."""
        # Get start and end of day
        start_of_day = datetime.combine(date.date(), datetime.min.time())
        end_of_day = datetime.combine(date.date(), datetime.max.time())
        
        # Build query
        query = {
            "user.id": user_id,
            "action_type": action_type,
            "created_at": {
                "$gte": start_of_day,
                "$lte": end_of_day
            }
        }
        
        # Get transactions
        cursor = self.collection.find(query)
        transactions = await cursor.to_list(length=None)
        
        return [KarmaTransaction(**t) for t in transactions]
        
    async def get_top_users(
        self,
        limit: int = 10,
        domain: Optional[str] = None
    ) -> List[dict]:
        """Get top users by total karma points."""
        # Build match stage
        match = {}
        if domain:
            match["domain"] = domain
            
        # Aggregate points by user
        pipeline = [
            {"$match": match},
            {"$group": {
                "_id": "$user.id",
                "total_points": {"$sum": "$points"},
                "user": {"$first": "$user"}
            }},
            {"$sort": {"total_points": -1}},
            {"$limit": limit}
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=None)
        return result
