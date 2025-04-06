"""Karma related jobs."""
from app.db.repositories.karma_repository import KarmaRepository

class KarmaJobs:
    """Jobs for managing karma operations."""
    
    def __init__(self, karma_repository: KarmaRepository):
        """Initialize with repository."""
        self.karma_repository = karma_repository
    
    async def calculate_daily_karma(self):
        """Calculate daily karma for all users."""
        return await self.karma_repository.calculate_daily_karma()
    
    async def calculate_domain_karma(self, domain: str):
        """Calculate domain karma for all users."""
        return await self.karma_repository.calculate_domain_karma(domain) 