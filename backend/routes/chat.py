"""
Chat API routes with MongoDB
"""
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from bson import ObjectId
from database import get_conversations_collection, get_messages_collection
from schemas import (
    ChatRequest, ChatResponse,
    ConversationCreate, ConversationResponse, ConversationListResponse,
    MessageResponse
)
from services.ai_service import ai_service
from services.data_service import data_service

router = APIRouter(prefix="/api", tags=["chat"])


def serialize_doc(doc):
    """Convert MongoDB document to dict with string ID"""
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message and get AI response
    Creates a new conversation if conversation_id is not provided
    """
    try:
        conversations_col = get_conversations_collection()
        messages_col = get_messages_collection()
        
        # Get or create conversation
        if request.conversation_id:
            conversation = await conversations_col.find_one({"_id": ObjectId(request.conversation_id)})
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
            conversation_id = request.conversation_id
        else:
            # Create new conversation
            title = request.message[:50] + "..." if len(request.message) > 50 else request.message
            new_conversation = {
                "title": title,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            result = await conversations_col.insert_one(new_conversation)
            conversation_id = str(result.inserted_id)
        
        # Save user message
        user_message_doc = {
            "conversation_id": conversation_id,
            "role": "user",
            "content": request.message,
            "created_at": datetime.utcnow()
        }
        user_result = await messages_col.insert_one(user_message_doc)
        user_message_doc["_id"] = user_result.inserted_id
        
        # Get employee data
        employee_data = data_service.get_formatted_data()
        
        # Generate AI response
        ai_response_text = ai_service.generate_response(request.message, employee_data)
        
        # Save assistant message
        assistant_message_doc = {
            "conversation_id": conversation_id,
            "role": "assistant",
            "content": ai_response_text,
            "created_at": datetime.utcnow()
        }
        assistant_result = await messages_col.insert_one(assistant_message_doc)
        assistant_message_doc["_id"] = assistant_result.inserted_id
        
        # Update conversation timestamp
        await conversations_col.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"updated_at": datetime.utcnow()}}
        )
        
        return ChatResponse(
            conversation_id=conversation_id,
            user_message=MessageResponse(
                id=str(user_message_doc["_id"]),
                conversation_id=conversation_id,
                role=user_message_doc["role"],
                content=user_message_doc["content"],
                created_at=user_message_doc["created_at"]
            ),
            assistant_message=MessageResponse(
                id=str(assistant_message_doc["_id"]),
                conversation_id=conversation_id,
                role=assistant_message_doc["role"],
                content=assistant_message_doc["content"],
                created_at=assistant_message_doc["created_at"]
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations", response_model=List[ConversationListResponse])
async def get_conversations():
    """Get all conversations"""
    conversations_col = get_conversations_collection()
    conversations = await conversations_col.find().sort("updated_at", -1).to_list(100)
    
    return [
        ConversationListResponse(
            id=str(conv["_id"]),
            title=conv["title"],
            created_at=conv["created_at"],
            updated_at=conv["updated_at"]
        )
        for conv in conversations
    ]


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: str):
    """Get a specific conversation with all messages"""
    conversations_col = get_conversations_collection()
    messages_col = get_messages_collection()
    
    try:
        conversation = await conversations_col.find_one({"_id": ObjectId(conversation_id)})
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get messages for this conversation
        messages = await messages_col.find({"conversation_id": conversation_id}).sort("created_at", 1).to_list(1000)
        
        return ConversationResponse(
            id=str(conversation["_id"]),
            title=conversation["title"],
            created_at=conversation["created_at"],
            updated_at=conversation["updated_at"],
            messages=[
                MessageResponse(
                    id=str(msg["_id"]),
                    conversation_id=conversation_id,
                    role=msg["role"],
                    content=msg["content"],
                    created_at=msg["created_at"]
                )
                for msg in messages
            ]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(conversation: ConversationCreate):
    """Create a new conversation"""
    conversations_col = get_conversations_collection()
    
    new_conversation = {
        "title": conversation.title,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = await conversations_col.insert_one(new_conversation)
    
    return ConversationResponse(
        id=str(result.inserted_id),
        title=new_conversation["title"],
        created_at=new_conversation["created_at"],
        updated_at=new_conversation["updated_at"],
        messages=[]
    )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation and all its messages"""
    conversations_col = get_conversations_collection()
    messages_col = get_messages_collection()
    
    try:
        # Delete conversation
        result = await conversations_col.delete_one({"_id": ObjectId(conversation_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Delete all messages in this conversation
        await messages_col.delete_many({"conversation_id": conversation_id})
        
        return {"message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
