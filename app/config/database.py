# Database connection configuration

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .settings import settings
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)

class Database:
    def __init__(self) -> None:
        # Initialize without type hints in assignment
        self.client = None  
        self._db = None

    def get_client(self) -> Optional[Any]:
        """Get the database client."""
        return self.client

    def get_db(self) -> Optional[Any]:
        """Get the database instance."""
        return self._db
    
    async def connect(self) -> None:
        """Create database connection."""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            self._db = self.client[settings.MONGODB_DB]
            logger.info("Connected to MongoDB.")
            
            # Verify connection
            await self.client.admin.command('ping')
            logger.info("MongoDB connection verified.")
            
        except Exception as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise
    
    async def close(self) -> None:
        """Close database connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")
    
    @property
    def db(self) -> Optional[Any]:
        """Return database instance."""
        return self._db

# Create a global database instance
db = Database()

# Export database instance
__all__ = ["db"]
