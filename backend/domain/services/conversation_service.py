"""
Conversation service - Business logic for conversations
"""
from typing import List, Optional
from domain.models import Conversation
from domain.repositories import ConversationRepository, MessageRepository
from core.exceptions import NotFoundException, ValidationException
from core.logging_config import get_logger

logger = get_logger(__name__)


class ConversationService:
    """Service for conversation business logic"""
    
    def __init__(
        self,
        conversation_repo: ConversationRepository,
        message_repo: MessageRepository
    ):
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo
    
    async def create_conversation(self, title: str) -> Conversation:
        """
        Create a new conversation
        
        Args:
            title: Conversation title
            
        Returns:
            Created conversation with ID
        """
        if not title or not title.strip():
            raise ValidationException("Conversation title cannot be empty")
        
        conversation = Conversation.create_new(title.strip())
        conversation_id = await self.conversation_repo.create(conversation)
        conversation.id = conversation_id
        
        logger.info(f"Created conversation: {conversation_id}")
        return conversation
    
    async def get_conversation(self, conversation_id: str) -> Conversation:
        """
        Get conversation by ID
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Conversation
            
        Raises:
            NotFoundException: If conversation not found
        """
        conversation = await self.conversation_repo.get_by_id(conversation_id)
        if not conversation:
            raise NotFoundException(f"Conversation not found", {"id": conversation_id})
        
        return conversation
    
    async def list_conversations(self, limit: int = 100) -> List[Conversation]:
        """
        List all conversations
        
        Args:
            limit: Maximum number of conversations to return
            
        Returns:
            List of conversations
        """
        return await self.conversation_repo.list_all(limit)
    
    async def delete_conversation(self, conversation_id: str) -> None:
        """
        Delete a conversation and all its messages
        
        Args:
            conversation_id: Conversation ID
            
        Raises:
            NotFoundException: If conversation not found
        """
        # Verify conversation exists
        await self.get_conversation(conversation_id)
        
        # Delete all messages
        deleted_count = await self.message_repo.delete_by_conversation(conversation_id)
        logger.info(f"Deleted {deleted_count} messages for conversation {conversation_id}")
        
        # Delete conversation
        deleted = await self.conversation_repo.delete(conversation_id)
        if not deleted:
            raise NotFoundException(f"Conversation not found", {"id": conversation_id})
        
        logger.info(f"Deleted conversation: {conversation_id}")
    
    async def update_conversation_timestamp(self, conversation_id: str) -> None:
        """Update conversation's updated_at timestamp"""
        await self.conversation_repo.update_timestamp(conversation_id)
