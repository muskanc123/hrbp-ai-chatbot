"""
MongoDB database connection and collections
"""
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
import asyncio

# MongoDB client
client = None
database = None

# Collections
conversations_collection = None
messages_collection = None


async def connect_to_mongo():
    """Connect to MongoDB"""
    global client, database, conversations_collection, messages_collection
    
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        database = client[settings.MONGODB_DB_NAME]
        
        # Get collections
        conversations_collection = database["conversations"]
        messages_collection = database["messages"]
        
        # Create indexes
        await conversations_collection.create_index("created_at")
        await conversations_collection.create_index("updated_at")
        await messages_collection.create_index("conversation_id")
        await messages_collection.create_index("created_at")
        
        # Test connection
        await client.admin.command('ping')
        print("✓ Connected to MongoDB successfully")
        
    except Exception as e:
        print(f"✗ Error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("✓ MongoDB connection closed")


def get_database():
    """Get database instance"""
    return database


def get_conversations_collection():
    """Get conversations collection"""
    return conversations_collection


def get_messages_collection():
    """Get messages collection"""
    return messages_collection
