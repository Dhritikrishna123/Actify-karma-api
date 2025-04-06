# Karma data operations

from typing import Optional, List, Dict
from datetime import datetime, UTC
from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...models.karma import KarmaTransaction, KarmaTransactionCreate, KarmaScore
from ...models.karma_action import KarmaActionType
from ...models.user import UserReference
from ..mongodb import mongodb

class KarmaRepository:
    """Repository for karma-related database operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase = None):
        """Initialize repository with database connection."""
        self.db = db if db is not None else mongodb.get_db()
        self.collection = self.db.karma_transactions
        
    async def create_transaction(self, transaction: KarmaTransactionCreate) -> KarmaTransaction:
        """Create a new karma transaction."""
        # Convert to dict and add timestamps
        transaction_dict = transaction.dict()
        transaction_dict["created_at"] = datetime.now(UTC)
        transaction_dict["updated_at"] = datetime.now(UTC)
        
        # Insert into database
        result = await self.collection.insert_one(transaction_dict)
        
        # Add ID and return as KarmaTransaction
        transaction_dict["_id"] = result.inserted_id
        return KarmaTransaction(**transaction_dict)
        
    async def get_user_karma_score(self, user_id: str) -> KarmaScore:
        """Get current karma score for a user."""
        # Calculate overall score
        overall_pipeline = [
            {"$match": {"user.core_user_id": user_id}},
            {"$group": {"_id": None, "total": {"$sum": "$points"}}}
        ]
        
        overall_result = await self.collection.aggregate(overall_pipeline).to_list(length=1)
        overall_score = overall_result[0]["total"] if overall_result else 0.0
        
        # Calculate domain scores
        domain_pipeline = [
            {"$match": {"user.core_user_id": user_id}},
            {"$group": {
                "_id": "$domain",
                "score": {"$sum": "$points"}
            }}
        ]
        
        domain_results = await self.collection.aggregate(domain_pipeline).to_list(length=None)
        domain_scores = {doc["_id"]: doc["score"] for doc in domain_results} if domain_results else {}
        
        return KarmaScore(
            overall_score=overall_score,
            domain_scores=domain_scores
        )
        
    async def get_user_karma_history(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[KarmaTransaction]:
        """Get karma transaction history for a user."""
        # Build query
        query = {"user.core_user_id": user_id}
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
        
    async def get_user_domain_karma(
        self,
        user_id: str,
        domain: str
    ) -> float:
        """Get karma score for a user in a specific domain."""
        pipeline = [
            {
                "$match": {
                    "user.core_user_id": user_id,
                    "domain": domain
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$points"}
                }
            }
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0.0
        
    async def get_user_domain_history(
        self,
        user_id: str,
        domain: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[KarmaTransaction]:
        """Get karma transaction history for a user in a specific domain."""
        # Build query
        query = {
            "user.core_user_id": user_id,
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
        
    async def get_top_karma_users(
        self,
        limit: int = 10,
        domain: Optional[str] = None
    ) -> List[dict]:
        """Get top users by karma points."""
        # Build match stage
        match = {}
        if domain:
            match["domain"] = domain
            
        # Aggregate points by user
        pipeline = [
            {"$match": match},
            {
                "$group": {
                    "_id": "$user.core_user_id",
                    "total_points": {"$sum": "$points"},
                    "user": {"$first": "$user"}
                }
            },
            {"$sort": {"total_points": -1}},
            {"$limit": limit}
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=None)
        return result
