"""
AstraCalc Agent Server - Main Application
FastAPI + Pydantic AI

Level 0: Hello World Agent
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Optional
import logging

from agent import create_agent
from config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AstraCalc Agent Server",
    description="AI-powered astrology assistant",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
agent = create_agent()


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    model: str


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str


# Routes
@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "service": "AstraCalc Agent Server",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        environment=settings.ENVIRONMENT
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint - Level 0
    Simple synchronous chat without tools
    """
    try:
        logger.info(f"Received message: {request.message[:50]}...")
        
        # Run agent (synchronous for Level 0)
        result = agent.run_sync(request.message)
        
        logger.info(f"Agent response: {result.data[:50]}...")
        
        return ChatResponse(
            response=result.data,
            model=settings.ANTHROPIC_MODEL
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Run server (for local development)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development"
    )