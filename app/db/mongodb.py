# MongoDB connection and helper functions

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDB:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance

    async def connect_to_database(self):
        """Connect to MongoDB Atlas."""
        try:
            # MongoDB Atlas connection string
            mongo_url = os.getenv("MONGODB_URL")
            if not mongo_url:
                raise ValueError("MONGODB_URL environment variable not set")

            # Create client with connection settings
            self._client = AsyncIOMotorClient(
                mongo_url,
                serverSelectionTimeoutMS=10000,  # 10 second timeout
                maxPoolSize=50,
                minPoolSize=10,
                retryWrites=True
            )

            # Verify connection with a ping
            await self._client.admin.command('ping')
            
            # Get database instance
            db_name = os.getenv("MONGODB_DB", "karma_db")
            self._db = self._client[db_name]
            
            logger.info(f"Successfully connected to MongoDB Atlas! Database: {db_name}")
            return True
        except Exception as e:
            logger.error(f"Could not connect to MongoDB Atlas: {str(e)}")
            # Don't raise the exception, just log it
            self._client = None
            self._db = None
            return False

    async def close_database_connection(self):
        """Close the database connection."""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("MongoDB connection closed")

    def get_db(self):
        """Get the database instance."""
        if self._db is None:
            logger.warning("Database not connected. Please call connect_to_database() first.")
            return None
        return self._db

# Create a single instance of MongoDB
mongodb = MongoDB()

# Export the instance
__all__ = ["mongodb"]
