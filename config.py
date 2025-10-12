"""
AstraCalc Agent Server - Configuration

Manages environment variables and application settings
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Core
    ENVIRONMENT: str = "production"
    PORT: int = 8585  
    LOG_LEVEL: str = "INFO"
    
    # Anthropic
    ANTHROPIC_API_KEY: str
    ANTHROPIC_MODEL="claude-sonnet-4.5-20250929"
    ANTHROPIC_MODEL_FAST: str = "claude-haiku-4"
    
    # Redis (for future levels)
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Zep Memory (for future levels)
    ZEP_API_KEY: str = "placeholder"
    ZEP_API_URL: str = "https://api.getzep.com"
    
    # Calculation Engine (for future levels)
    CALC_ENGINE_URL: str = "https://calc.yourdomain.com"
    CALC_ENGINE_API_KEY: str = "placeholder"
    
    # Monitoring (optional)
    LOGFIRE_API_KEY: str = "placeholder"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Security
    SECRET_KEY: str = "change-this-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()


# Validate critical settings
def validate_settings():
    """Validates that critical settings are present"""
    errors = []
    
    if not settings.ANTHROPIC_API_KEY or settings.ANTHROPIC_API_KEY == "sk-ant-api03-xxx":
        errors.append("ANTHROPIC_API_KEY not configured")
    
    if settings.SECRET_KEY == "change-this-in-production" and settings.ENVIRONMENT == "production":
        errors.append("SECRET_KEY must be changed in production")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    return True


# Run validation
if __name__ == "__main__":
    try:
        validate_settings()
        print("✅ Configuration valid!")
        print(f"Environment: {settings.ENVIRONMENT}")
        print(f"Model: {settings.ANTHROPIC_MODEL}")
        print(f"Port: {settings.PORT}")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
