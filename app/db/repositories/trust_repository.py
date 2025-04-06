# Trust data operations

from typing import Optional, List, Dict
from datetime import datetime, UTC
from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...models.trust import TrustScore, TrustScoreCreate, TrustMetric
from ...models.user import UserReference
from ...db.mongodb import mongodb

class TrustRepository:
    """Repository for trust-related database operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase = None):
        """Initialize repository with database connection."""
        self.db = db if db is not None else mongodb.get_db()
        self.collection = self.db.trust_scores
        
    async def create_trust_score(self, trust_score: TrustScoreCreate) -> TrustScore:
        """Create a new trust score."""
        # Convert to dict and add timestamps
        trust_dict = trust_score.dict()
        trust_dict["created_at"] = datetime.now(UTC)
        trust_dict["updated_at"] = datetime.now(UTC)
        
        # Insert into database
        result = await self.collection.insert_one(trust_dict)
        
        # Add ID and return as TrustScore
        trust_dict["id"] = str(result.inserted_id)
        trust_dict["_id"] = result.inserted_id
        return TrustScore(**trust_dict)
        
    async def get_user_trust_score(
        self,
        user_id: str
    ) -> Optional[TrustScore]:
        """Get current trust score for a user."""
        # Get latest trust score
        cursor = self.collection.find(
            {"user.core_user_id": user_id}
        ).sort("created_at", -1).limit(1)
        
        result = await cursor.to_list(length=1)
        if not result:
            return None
            
        result[0]["id"] = str(result[0]["_id"])
        return TrustScore(**result[0])
        
    async def get_user_trust_history(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[TrustScore]:
        """Get trust score history for a user."""
        # Build query
        query = {"user.id": user_id}
        if start_date or end_date:
            query["created_at"] = {}
            if start_date:
                query["created_at"]["$gte"] = start_date
            if end_date:
                query["created_at"]["$lte"] = end_date
                
        # Get scores
        cursor = self.collection.find(query).sort("created_at", -1)
        scores = await cursor.to_list(length=None)
        
        return [TrustScore(**s) for s in scores]
        
    async def get_trust_metrics(
        self,
        user_id: str
    ) -> Dict[str, float]:
        """Get detailed trust metrics for a user."""
        # Get latest trust score
        cursor = self.collection.find(
            {"user.id": user_id}
        ).sort("created_at", -1).limit(1)
        
        result = await cursor.to_list(length=1)
        if not result:
            return {}
            
        trust_score = TrustScore(**result[0])
        return trust_score.metrics
        
    async def update_trust_metric(
        self,
        user_id: str,
        metric_name: str,
        value: float
    ) -> TrustScore:
        """Update a specific trust metric for a user."""
        # Get current trust score
        current_score = await self.get_user_trust_score(user_id)
        if not current_score:
            # Create new trust score if none exists
            new_score = TrustScoreCreate(
                user=UserReference(core_user_id=user_id),
                overall_score=0.0,
                metrics={metric_name: value}
            )
            return await self.create_trust_score(new_score)
            
        # Update metric in current score
        current_score.metrics[metric_name] = value
        
        # Recalculate overall score
        current_score.overall_score = sum(current_score.metrics.values()) / len(current_score.metrics)
        
        # Create new trust score with updated values
        new_score = TrustScoreCreate(
            user=current_score.user,
            overall_score=current_score.overall_score,
            metrics=current_score.metrics
        )
        
        return await self.create_trust_score(new_score)
        
    async def get_top_trusted_users(
        self,
        limit: int = 10,
        metric: Optional[str] = None
    ) -> List[dict]:
        """Get top users by trust score."""
        # Build match stage
        match = {}
        if metric:
            match[f"metrics.{metric}"] = {"$exists": True}
            
        # Aggregate scores by user
        pipeline = [
            {"$match": match},
            {"$sort": {"created_at": -1}},
            {"$group": {
                "_id": "$user.id",
                "overall_score": {"$first": "$overall_score"},
                "metrics": {"$first": "$metrics"},
                "user": {"$first": "$user"}
            }},
            {"$sort": {"overall_score": -1}},
            {"$limit": limit}
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=None)
        return result
