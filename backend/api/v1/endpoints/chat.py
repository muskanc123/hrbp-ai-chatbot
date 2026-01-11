"""
Simplified chat routes using service layer
"""
from fastapi import APIRouter, Depends
from typing import List

from schemas import (
    ChatRequest, ChatResponse,
    ConversationCreate, ConversationResponse, ConversationListResponse,
    MessageResponse
)
from domain.services import ConversationService, MessageService, ChatService
from core.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["chat"])


# Dependency injection (will be properly configured in main.py)
def get_chat_service() -> ChatService:
    """Get chat service instance - placeholder for DI"""
    from main import get_services
    services = get_services()
    return services['chat_service']


def get_conversation_service() -> ConversationService:
    """Get conversation service instance - placeholder for DI"""
    from main import get_services
    services = get_services()
    return services['conversation_service']


def get_message_service() -> MessageService:
    """Get message service instance - placeholder for DI"""
    from main import get_services
    services = get_services()
    return services['message_service']


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Send a message and get AI response
    Creates a new conversation if conversation_id is not provided
    """
    logger.info(f"Chat request received")
    
    conversation_id, user_msg, assistant_msg = await chat_service.process_chat_message(
        user_message=request.message,
        conversation_id=request.conversation_id
    )
    
    return ChatResponse(
        conversation_id=conversation_id,
        user_message=MessageResponse(
            id=user_msg.id,
            conversation_id=user_msg.conversation_id,
            role=user_msg.role,
            content=user_msg.content,
            created_at=user_msg.created_at
        ),
        assistant_message=MessageResponse(
            id=assistant_msg.id,
            conversation_id=assistant_msg.conversation_id,
            role=assistant_msg.role,
            content=assistant_msg.content,
            created_at=assistant_msg.created_at
        )
    )


@router.get("/conversations", response_model=List[ConversationListResponse])
async def get_conversations(
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """Get all conversations"""
    logger.info("Get conversations request")
    
    conversations = await conversation_service.list_conversations()
    
    return [
        ConversationListResponse(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at
        )
        for conv in conversations
    ]


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    conversation_service: ConversationService = Depends(get_conversation_service),
    message_service: MessageService = Depends(get_message_service)
):
    """Get a specific conversation with all messages"""
    logger.info(f"Get conversation request: {conversation_id}")
    
    conversation = await conversation_service.get_conversation(conversation_id)
    messages = await message_service.get_conversation_messages(conversation_id)
    
    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=[
            MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            )
            for msg in messages
        ]
    )


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """Create a new conversation"""
    logger.info(f"Create conversation request: {conversation.title}")
    
    new_conversation = await conversation_service.create_conversation(conversation.title)
    
    return ConversationResponse(
        id=new_conversation.id,
        title=new_conversation.title,
        created_at=new_conversation.created_at,
        updated_at=new_conversation.updated_at,
        messages=[]
    )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """Delete a conversation and all its messages"""
    logger.info(f"Delete conversation request: {conversation_id}")
    
    await conversation_service.delete_conversation(conversation_id)
    
    return {"message": "Conversation deleted successfully"}
