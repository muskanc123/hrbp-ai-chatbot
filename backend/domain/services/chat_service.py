"""
Chat service - Orchestrates chat flow
"""
from typing import Tuple
from domain.models import Conversation, Message
from domain.services.conversation_service import ConversationService
from domain.services.message_service import MessageService
from core.exceptions import ValidationException
from core.logging_config import get_logger

logger = get_logger(__name__)


class ChatService:
    """Service for chat orchestration"""
    
    def __init__(
        self,
        conversation_service: ConversationService,
        message_service: MessageService,
        ai_service,  # Will be typed when we refactor AI service
        data_service  # Will be typed when we refactor data service
    ):
        self.conversation_service = conversation_service
        self.message_service = message_service
        self.ai_service = ai_service
        self.data_service = data_service
    
    async def process_chat_message(
        self,
        user_message: str,
        conversation_id: str = None
    ) -> Tuple[str, Message, Message]:
        """
        Process a chat message and generate AI response
        
        Args:
            user_message: User's message
            conversation_id: Optional conversation ID (creates new if None)
            
        Returns:
            Tuple of (conversation_id, user_message, assistant_message)
        """
        # Validate input
        if not user_message or not user_message.strip():
            raise ValidationException("Message cannot be empty")
        
        user_message = user_message.strip()
        
        # Get or create conversation
        if conversation_id:
            conversation = await self.conversation_service.get_conversation(conversation_id)
        else:
            # Create new conversation with message as title
            title = user_message[:50] + "..." if len(user_message) > 50 else user_message
            conversation = await self.conversation_service.create_conversation(title)
            conversation_id = conversation.id
        
        logger.info(f"Processing chat message for conversation: {conversation_id}")
        
        # Save user message
        user_msg = await self.message_service.create_message(
            conversation_id=conversation_id,
            role="user",
            content=user_message
        )
        
        # Get employee data
        employee_data = self.data_service.get_formatted_data()
        
        # Generate AI response
        ai_response_text = self.ai_service.generate_response(user_message, employee_data)
        
        # Save assistant message
        assistant_msg = await self.message_service.create_message(
            conversation_id=conversation_id,
            role="assistant",
            content=ai_response_text
        )
        
        # Update conversation timestamp
        await self.conversation_service.update_conversation_timestamp(conversation_id)
        
        logger.info(f"Chat message processed successfully for conversation: {conversation_id}")
        
        return conversation_id, user_msg, assistant_msg
