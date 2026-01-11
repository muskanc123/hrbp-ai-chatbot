"""
Message service - Business logic for messages
"""
from typing import List
from domain.models import Message
from domain.repositories import MessageRepository
from core.exceptions import ValidationException
from core.logging_config import get_logger

logger = get_logger(__name__)


class MessageService:
    """Service for message business logic"""
    
    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo
    
    async def create_message(
        self,
        conversation_id: str,
        role: str,
        content: str
    ) -> Message:
        """
        Create a new message
        
        Args:
            conversation_id: Conversation ID
            role: Message role ("user" or "assistant")
            content: Message content
            
        Returns:
            Created message with ID
        """
        # Validate inputs
        if not conversation_id or not conversation_id.strip():
            raise ValidationException("Conversation ID cannot be empty")
        
        if role not in ["user", "assistant"]:
            raise ValidationException(
                "Invalid role",
                {"role": role, "allowed": ["user", "assistant"]}
            )
        
        if not content or not content.strip():
            raise ValidationException("Message content cannot be empty")
        
        # Create message
        message = Message.create_new(
            conversation_id=conversation_id.strip(),
            role=role,
            content=content.strip()
        )
        
        message_id = await self.message_repo.create(message)
        message.id = message_id
        
        logger.info(f"Created {role} message: {message_id}")
        return message
    
    async def get_conversation_messages(
        self,
        conversation_id: str,
        limit: int = 1000
    ) -> List[Message]:
        """
        Get all messages for a conversation
        
        Args:
            conversation_id: Conversation ID
            limit: Maximum number of messages
            
        Returns:
            List of messages ordered by creation time
        """
        return await self.message_repo.get_by_conversation(conversation_id, limit)
