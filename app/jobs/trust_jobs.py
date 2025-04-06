"""Trust related jobs."""
from app.db.repositories.trust_repository import TrustRepository

class TrustJobs:
    """Jobs for managing trust operations."""
    
    def __init__(self, trust_repository: TrustRepository):
        """Initialize with repository."""
        self.trust_repository = trust_repository
    
    async def calculate_daily_trust_scores(self):
        """Calculate daily trust scores for all users."""
        return await self.trust_repository.calculate_daily_trust_scores()
    
    async def calculate_trust_metrics(self):
        """Calculate trust metrics for the period."""
        return await self.trust_repository.calculate_trust_metrics()
    
    async def update_trust_scores(self):
        """Update trust scores based on recent activity."""
        return await self.trust_repository.update_trust_scores() 