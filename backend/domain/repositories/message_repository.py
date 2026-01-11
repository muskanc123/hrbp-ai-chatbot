"""
Message repository implementation
"""
from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from domain.models import Message
from domain.repositories.base import IRepository
from core.exceptions import DatabaseException, NotFoundException
from core.logging_config import get_logger

logger = get_logger(__name__)


class MessageRepository(IRepository[Message]):
    """MongoDB implementation of message repository"""
    
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
    
    async def create(self, message: Message) -> str:
        """Create a new message"""
        try:
            doc = {
                "conversation_id": message.conversation_id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at
            }
            result = await self.collection.insert_one(doc)
            logger.info(f"Created message: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to create message: {e}")
            raise DatabaseException("Failed to create message", {"error": str(e)})
    
    async def get_by_id(self, id: str) -> Optional[Message]:
        """Get message by ID"""
        try:
            doc = await self.collection.find_one({"_id": ObjectId(id)})
            if not doc:
                return None
            
            return Message(
                id=str(doc["_id"]),
                conversation_id=doc["conversation_id"],
                role=doc["role"],
                content=doc["content"],
                created_at=doc["created_at"]
            )
        except Exception as e:
            logger.error(f"Failed to get message {id}: {e}")
            raise DatabaseException(f"Failed to get message", {"id": id, "error": str(e)})
    
    async def update(self, id: str, message: Message) -> None:
        """Update message"""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {
                    "content": message.content
                }}
            )
            if result.matched_count == 0:
                raise NotFoundException(f"Message not found", {"id": id})
            
            logger.info(f"Updated message: {id}")
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Failed to update message {id}: {e}")
            raise DatabaseException("Failed to update message", {"id": id, "error": str(e)})
    
    async def delete(self, id: str) -> bool:
        """Delete message"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(id)})
            deleted = result.deleted_count > 0
            if deleted:
                logger.info(f"Deleted message: {id}")
            return deleted
        except Exception as e:
            logger.error(f"Failed to delete message {id}: {e}")
            raise DatabaseException("Failed to delete message", {"id": id, "error": str(e)})
    
    async def list_all(self, limit: int = 100) -> List[Message]:
        """List all messages (not typically used)"""
        try:
            cursor = self.collection.find().limit(limit)
            docs = await cursor.to_list(length=limit)
            
            return [
                Message(
                    id=str(doc["_id"]),
                    conversation_id=doc["conversation_id"],
                    role=doc["role"],
                    content=doc["content"],
                    created_at=doc["created_at"]
                )
                for doc in docs
            ]
        except Exception as e:
            logger.error(f"Failed to list messages: {e}")
            raise DatabaseException("Failed to list messages", {"error": str(e)})
    
    async def get_by_conversation(self, conversation_id: str, limit: int = 1000) -> List[Message]:
        """Get all messages for a conversation"""
        try:
            cursor = self.collection.find(
                {"conversation_id": conversation_id}
            ).sort("created_at", 1).limit(limit)
            
            docs = await cursor.to_list(length=limit)
            
            return [
                Message(
                    id=str(doc["_id"]),
                    conversation_id=doc["conversation_id"],
                    role=doc["role"],
                    content=doc["content"],
                    created_at=doc["created_at"]
                )
                for doc in docs
            ]
        except Exception as e:
            logger.error(f"Failed to get messages for conversation {conversation_id}: {e}")
            raise DatabaseException("Failed to get messages", {"conversation_id": conversation_id, "error": str(e)})
    
    async def delete_by_conversation(self, conversation_id: str) -> int:
        """Delete all messages for a conversation"""
        try:
            result = await self.collection.delete_many({"conversation_id": conversation_id})
            logger.info(f"Deleted {result.deleted_count} messages for conversation {conversation_id}")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Failed to delete messages for conversation {conversation_id}: {e}")
            raise DatabaseException("Failed to delete messages", {"conversation_id": conversation_id, "error": str(e)})
