"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


# Message Schemas
class MessageBase(BaseModel):
    role: str
    content: str


class MessageCreate(MessageBase):
    conversation_id: str


class MessageResponse(MessageBase):
    id: str
    conversation_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Conversation Schemas
class ConversationBase(BaseModel):
    title: str


class ConversationCreate(ConversationBase):
    pass


class ConversationResponse(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True


class ConversationListResponse(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Chat Schemas
class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    conversation_id: str
    user_message: MessageResponse
    assistant_message: MessageResponse


# Health Check
class HealthResponse(BaseModel):
    status: str
    database: str
    employee_data_loaded: bool
