"""
Configuration settings for AstraCalc Agent Server

Level 2: Added Calculation Engine and N8N Webhook URLs
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Server
    PORT: int = int(os.getenv("PORT", "8585"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    
    # Anthropic
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
    
    # Calculation Engine
    CALCULATION_ENGINE_URL: str = os.getenv(
        "CALCULATION_ENGINE_URL", 
        "https://engine.hasanpercin.xyz"
    )
    CALCULATION_ENGINE_API_KEY: str = os.getenv("CALCULATION_ENGINE_API_KEY", "")
    
    # N8N Webhook for Reports
    N8N_WEBHOOK_URL: str = os.getenv(
        "N8N_WEBHOOK_URL",
        "https://n8n.hasanpercin.xyz/webhook-test/c33b37b1-46ef-4cd2-807c-594a3f329719"
    )
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
