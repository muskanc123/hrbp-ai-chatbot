"""
Base repository interface
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """Base repository interface"""
    
    @abstractmethod
    async def create(self, entity: T) -> str:
        """Create a new entity and return its ID"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    async def update(self, id: str, entity: T) -> None:
        """Update an existing entity"""
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete an entity by ID, return True if deleted"""
        pass
    
    @abstractmethod
    async def list_all(self, limit: int = 100) -> List[T]:
        """List all entities with optional limit"""
        pass
