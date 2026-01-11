"""
Custom exception classes for the chatbot application
"""


class ChatbotException(Exception):
    """Base exception for all chatbot errors"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class DatabaseException(ChatbotException):
    """Raised when database operations fail"""
    pass


class AIServiceException(ChatbotException):
    """Raised when AI service operations fail"""
    pass


class ValidationException(ChatbotException):
    """Raised when input validation fails"""
    pass


class NotFoundException(ChatbotException):
    """Raised when a requested resource is not found"""
    pass


class ConfigurationException(ChatbotException):
    """Raised when configuration is invalid or missing"""
    pass
