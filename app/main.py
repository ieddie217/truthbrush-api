from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.logging import setup_logging
from .core.auth import verify_basic_auth
from .api.endpoints import statuses

# Set up logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=f"{settings.API_DESCRIPTION} - All endpoints require HTTP Basic Authentication.",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(statuses.router, tags=["statuses"])

@app.get("/")
def root(auth_user: str = Depends(verify_basic_auth)):
    """Root endpoint with API information. Requires HTTP Basic Authentication."""
    return {
        "message": "Truthbrush API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "endpoints": {
            "statuses": "/statuses"
        },
        "authentication": "HTTP Basic Auth required for all endpoints"
    }

@app.get("/health")
def health_check(auth_user: str = Depends(verify_basic_auth)):
    """Health check endpoint. Requires HTTP Basic Authentication."""
    return {"status": "healthy", "authenticated_user": auth_user} 