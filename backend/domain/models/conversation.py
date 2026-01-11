"""
Domain model for Conversation
"""
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Conversation:
    """Conversation domain model"""
    id: Optional[str]
    title: str
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def create_new(cls, title: str) -> "Conversation":
        """Factory method to create a new conversation"""
        now = datetime.utcnow()
        return cls(
            id=None,
            title=title,
            created_at=now,
            updated_at=now
        )
