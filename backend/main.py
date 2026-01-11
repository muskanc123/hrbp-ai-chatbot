"""
FastAPI Main Application with Clean Architecture
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

# Core
from core import setup_logging, get_logger
from core.exceptions import ChatbotException

# Config
from config import settings

# Infrastructure
from database import connect_to_mongo, close_mongo_connection, get_conversations_collection, get_messages_collection
from infrastructure.ai import GeminiAIService

# Domain
from domain.repositories import ConversationRepository, MessageRepository
from domain.services import ConversationService, MessageService, ChatService

# API
from api.v1 import router as api_v1_router
from api.middleware.error_handler import register_exception_handlers

# Schemas
from schemas import HealthResponse

# Legacy services (to be refactored)
from services.data_service import data_service

# Setup logging
setup_logging(level="INFO")
logger = get_logger(__name__)

# Global services container (simple DI)
_services = {}


def get_services():
    """Get services container"""
    return _services


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown"""
    # Startup
    logger.info("=" * 60)
    logger.info("🚀 AI Chatbot Backend Server - Clean Architecture")
    logger.info("=" * 60)
    
    try:
        # Connect to MongoDB
        await connect_to_mongo()
        logger.info("✓ MongoDB connected and indexed")
        
        # Initialize repositories
        conversations_col = get_conversations_collection()
        messages_col = get_messages_collection()
        
        conversation_repo = ConversationRepository(conversations_col)
        message_repo = MessageRepository(messages_col)
        logger.info("✓ Repositories initialized")
        
        # Initialize AI service
        prompt_config_path = os.path.join(
            os.path.dirname(__file__),
            "config/prompts/hrbp_assistant.yaml"
        )
        ai_service = GeminiAIService(
            api_key=settings.GEMINI_API_KEY,
            prompt_config_path=prompt_config_path
        )
        logger.info("✓ AI service initialized")
        
        # Initialize domain services
        conversation_service = ConversationService(conversation_repo, message_repo)
        message_service = MessageService(message_repo)
        chat_service = ChatService(
            conversation_service,
            message_service,
            ai_service,
            data_service
        )
        logger.info("✓ Domain services initialized")
        
        # Store services in global container
        _services['conversation_repo'] = conversation_repo
        _services['message_repo'] = message_repo
        _services['ai_service'] = ai_service
        _services['conversation_service'] = conversation_service
        _services['message_service'] = message_service
        _services['chat_service'] = chat_service
        
        # Check data service
        if data_service.data_loaded:
            summary = data_service.get_summary()
            logger.info(f"✓ Employee data loaded: {summary['total_employees']} records")
        else:
            logger.warning("⚠️  Employee data not loaded")
        
        logger.info(f"📍 Server running on: http://localhost:{settings.BACKEND_PORT}")
        logger.info(f"📚 API Documentation: http://localhost:{settings.BACKEND_PORT}/docs")
        logger.info(f"🔄 Alternative docs: http://localhost:{settings.BACKEND_PORT}/redoc")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}", exc_info=True)
        raise
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down server...")
    await close_mongo_connection()


# Create FastAPI app
app = FastAPI(
    title="AI Chatbot API",
    description="HRBP AI Assistant with Clean Architecture",
    version="3.0.0",
    lifespan=lifespan
)

# Register exception handlers
register_exception_handlers(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_v1_router)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        from database import get_database
        db = get_database()
        if db is not None:
            await db.command('ping')
            db_status = "connected"
        else:
            db_status = "disconnected"
    except:
        db_status = "disconnected"
    
    return HealthResponse(
        status="healthy",
        database=db_status,
        employee_data_loaded=data_service.data_loaded
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Chatbot API with Clean Architecture",
        "version": "3.0.0",
        "architecture": "Clean Architecture with DDD",
        "docs": "/docs",
        "health": "/health",
        "api": "/api/v1"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.BACKEND_PORT,
        reload=True
    )
