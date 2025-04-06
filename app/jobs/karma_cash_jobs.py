"""Karma cash related jobs."""
from app.db.repositories.karma_cash_repository import KarmaCashRepository

class KarmaCashJobs:
    """Jobs for managing karma cash operations."""
    
    def __init__(self, karma_cash_repository: KarmaCashRepository):
        """Initialize with repository."""
        self.karma_cash_repository = karma_cash_repository
    
    async def calculate_daily_earnings(self):
        """Calculate daily earnings for all users."""
        return await self.karma_cash_repository.calculate_daily_earnings()
    
    async def calculate_top_earners(self):
        """Calculate top earners for the period."""
        return await self.karma_cash_repository.calculate_top_earners() 