# FastAPI application entry point

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.db.mongodb import mongodb
from app.api.v1.routers import karma_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Karma System API for managing karma points, cash, and trust scores",
    version="1.0.0",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    karma_router.router,
    prefix=settings.API_V1_STR,
    tags=["karma"]
)

@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection on startup."""
    await mongodb.connect_to_database()

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection on shutdown."""
    await mongodb.close_database_connection()

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Karma System API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
