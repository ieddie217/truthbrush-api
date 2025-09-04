from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import secrets
from .config import settings

security = HTTPBasic()
bearer_security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = settings.JWT_SECRET_KEY if hasattr(settings, 'JWT_SECRET_KEY') else "your-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_security)) -> str:
    """
    Verify JWT token and return username.
    
    Args:
        credentials: JWT Bearer token from the request
        
    Returns:
        str: The authenticated username
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate user with username and password.
    For this example, we'll use the same credentials as basic auth.
    In a real application, you'd check against a database.
    """
    correct_username = settings.API_USERNAME
    correct_password = settings.API_PASSWORD
    
    if not correct_username or not correct_password:
        return False
    
    # In a real app, you'd check the hashed password from database
    # For now, we'll just verify plain text password
    is_correct_username = secrets.compare_digest(username, correct_username)
    is_correct_password = secrets.compare_digest(password, correct_password)
    
    return is_correct_username and is_correct_password 