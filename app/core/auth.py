from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from .config import settings

security = HTTPBasic()

def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Verify HTTP Basic Authentication credentials.
    
    Args:
        credentials: HTTP Basic Auth credentials from the request
        
    Returns:
        str: The authenticated username
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Get credentials from environment variables
    correct_username = settings.API_USERNAME
    correct_password = settings.API_PASSWORD
    
    # Check if credentials are configured
    if not correct_username or not correct_password:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API authentication not configured",
        )
    
    # Verify credentials using secure comparison
    is_correct_username = secrets.compare_digest(credentials.username, correct_username)
    is_correct_password = secrets.compare_digest(credentials.password, correct_password)
    
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username 