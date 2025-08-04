import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings and configuration."""
    
    # API Settings
    API_TITLE = "Truthbrush API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "API for accessing Truth Social data via truthbrush"
    
    # API Authentication
    API_USERNAME = os.getenv("API_USERNAME", "admin")
    API_PASSWORD = os.getenv("API_PASSWORD", "password")
    
    # Server Settings
    HOST = "0.0.0.0"
    PORT = 8000
    RELOAD = True
    
    # Truth Social Credentials
    TRUTHSOCIAL_USERNAME = os.getenv("TRUTHSOCIAL_USERNAME")
    TRUTHSOCIAL_PASSWORD = os.getenv("TRUTHSOCIAL_PASSWORD")
    TRUTHSOCIAL_TOKEN = os.getenv("TRUTHSOCIAL_TOKEN")
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/truthbrush_api.log"
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
    
    # Data
    DATA_DIR = "data"

# Global settings instance
settings = Settings() 