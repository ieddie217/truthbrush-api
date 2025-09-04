from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.logging import setup_logging
from .core.auth import verify_basic_auth, verify_token
from .api.endpoints import statuses, auth

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
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(statuses.router, tags=["statuses"])

@app.get("/")
def root(auth_user: str = Depends(verify_token)):
    """Root endpoint with API information. Requires JWT Bearer Authentication."""
    return {
        "message": "Truthbrush API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "endpoints": {
            "statuses": "/statuses",
            "auth": "/auth",
            "protected": "/protected (JWT required)",
            "user_profile": "/user/profile (JWT required)"
        },
        "authentication": "JWT Bearer Token required"
    }

@app.get("/health")
def health_check(auth_user: str = Depends(verify_token)):
    """Health check endpoint. Requires JWT Bearer Authentication."""
    return {"status": "healthy", "authenticated_user": auth_user}


@app.get("/protected")
def protected_endpoint(auth_user: str = Depends(verify_token)):
    """JWT protected endpoint example."""
    return {
        "message": "This is a JWT protected endpoint",
        "authenticated_user": auth_user,
        "auth_type": "JWT Bearer Token"
    }


@app.get("/user/profile")
def get_user_profile(current_user: str = Depends(verify_token)):
    """Get user profile - JWT protected."""
    return {
        "username": current_user,
        "profile": {
            "email": f"{current_user}@example.com",
            "role": "user",
            "created_at": "2024-01-01T00:00:00Z"
        }
    } 