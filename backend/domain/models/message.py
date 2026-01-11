"""
Domain model for Message
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class Message:
    """Message domain model"""
    id: Optional[str]
    conversation_id: str
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime
    
    @classmethod
    def create_new(cls, conversation_id: str, role: str, content: str) -> "Message":
        """Factory method to create a new message"""
        return cls(
            id=None,
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
