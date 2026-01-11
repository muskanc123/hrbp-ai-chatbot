"""
Global error handling middleware
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from core.exceptions import (
    ChatbotException,
    DatabaseException,
    AIServiceException,
    ValidationException,
    NotFoundException,
)
from core.logging_config import get_logger
import traceback

logger = get_logger(__name__)


async def chatbot_exception_handler(request: Request, exc: ChatbotException) -> JSONResponse:
    """Handle custom chatbot exceptions"""
    logger.error(
        f"Chatbot exception: {exc.message}",
        extra={"details": exc.details, "path": request.url.path}
    )
    
    # Map exception types to HTTP status codes
    status_code_map = {
        NotFoundException: status.HTTP_404_NOT_FOUND,
        ValidationException: status.HTTP_400_BAD_REQUEST,
        DatabaseException: status.HTTP_500_INTERNAL_SERVER_ERROR,
        AIServiceException: status.HTTP_503_SERVICE_UNAVAILABLE,
    }
    
    status_code = status_code_map.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "message": exc.message,
                "type": exc.__class__.__name__,
            }
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors"""
    logger.warning(
        "Validation error",
        extra={"errors": exc.errors(), "path": request.url.path}
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Validation error",
                "type": "ValidationError",
                "details": exc.errors()
            }
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle HTTP exceptions"""
    logger.warning(
        f"HTTP exception: {exc.detail}",
        extra={"status_code": exc.status_code, "path": request.url.path}
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "type": "HTTPException",
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other exceptions"""
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "path": request.url.path,
            "traceback": traceback.format_exc()
        },
        exc_info=True
    )
    
    # Never expose internal error details to clients
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "An internal server error occurred. Please try again later.",
                "type": "InternalServerError",
            }
        }
    )


def register_exception_handlers(app):
    """Register all exception handlers with the FastAPI app"""
    app.add_exception_handler(ChatbotException, chatbot_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
