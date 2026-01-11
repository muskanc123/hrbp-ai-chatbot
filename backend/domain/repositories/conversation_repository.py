"""
Conversation repository implementation
"""
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from domain.models import Conversation
from domain.repositories.base import IRepository
from core.exceptions import DatabaseException, NotFoundException
from core.logging_config import get_logger

logger = get_logger(__name__)


class ConversationRepository(IRepository[Conversation]):
    """MongoDB implementation of conversation repository"""
    
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
    
    async def create(self, conversation: Conversation) -> str:
        """Create a new conversation"""
        try:
            doc = {
                "title": conversation.title,
                "created_at": conversation.created_at,
                "updated_at": conversation.updated_at
            }
            result = await self.collection.insert_one(doc)
            logger.info(f"Created conversation: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to create conversation: {e}")
            raise DatabaseException("Failed to create conversation", {"error": str(e)})
    
    async def get_by_id(self, id: str) -> Optional[Conversation]:
        """Get conversation by ID"""
        try:
            doc = await self.collection.find_one({"_id": ObjectId(id)})
            if not doc:
                return None
            
            return Conversation(
                id=str(doc["_id"]),
                title=doc["title"],
                created_at=doc["created_at"],
                updated_at=doc["updated_at"]
            )
        except Exception as e:
            logger.error(f"Failed to get conversation {id}: {e}")
            raise DatabaseException(f"Failed to get conversation", {"id": id, "error": str(e)})
    
    async def update(self, id: str, conversation: Conversation) -> None:
        """Update conversation"""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {
                    "title": conversation.title,
                    "updated_at": datetime.utcnow()
                }}
            )
            if result.matched_count == 0:
                raise NotFoundException(f"Conversation not found", {"id": id})
            
            logger.info(f"Updated conversation: {id}")
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Failed to update conversation {id}: {e}")
            raise DatabaseException("Failed to update conversation", {"id": id, "error": str(e)})
    
    async def delete(self, id: str) -> bool:
        """Delete conversation"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(id)})
            deleted = result.deleted_count > 0
            if deleted:
                logger.info(f"Deleted conversation: {id}")
            return deleted
        except Exception as e:
            logger.error(f"Failed to delete conversation {id}: {e}")
            raise DatabaseException("Failed to delete conversation", {"id": id, "error": str(e)})
    
    async def list_all(self, limit: int = 100) -> List[Conversation]:
        """List all conversations"""
        try:
            cursor = self.collection.find().sort("updated_at", -1).limit(limit)
            docs = await cursor.to_list(length=limit)
            
            return [
                Conversation(
                    id=str(doc["_id"]),
                    title=doc["title"],
                    created_at=doc["created_at"],
                    updated_at=doc["updated_at"]
                )
                for doc in docs
            ]
        except Exception as e:
            logger.error(f"Failed to list conversations: {e}")
            raise DatabaseException("Failed to list conversations", {"error": str(e)})
    
    async def update_timestamp(self, id: str) -> None:
        """Update the updated_at timestamp"""
        try:
            await self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"updated_at": datetime.utcnow()}}
            )
        except Exception as e:
            logger.error(f"Failed to update timestamp for conversation {id}: {e}")
            raise DatabaseException("Failed to update timestamp", {"id": id, "error": str(e)})
