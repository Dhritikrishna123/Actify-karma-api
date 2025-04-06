# Karma API routes

from typing import Any
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from ....db.mongodb import mongodb
from ....db.repositories.karma_repository import KarmaRepository
from ....db.repositories.karma_cash_repository import KarmaCashRepository
from ....db.repositories.trust_repository import TrustRepository

# Create main router
router = APIRouter(prefix="/karma", tags=["karma"])

# Dependency to get database instance
async def get_db():
    return mongodb.get_db()

# Dependency to get repositories
def get_karma_repository(db: Any = Depends(get_db)) -> KarmaRepository:
    return KarmaRepository(db)

def get_karma_cash_repository(db: Any = Depends(get_db)) -> KarmaCashRepository:
    return KarmaCashRepository(db)

def get_trust_repository(db: Any = Depends(get_db)) -> TrustRepository:
    return TrustRepository(db)

# Import and include sub-routers after defining dependencies
from .routes import karma_routes, karma_cash_routes, trust_routes

router.include_router(karma_routes.router)
router.include_router(karma_cash_routes.router)
router.include_router(trust_routes.router) 