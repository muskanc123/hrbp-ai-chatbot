"""API v1 router"""
from fastapi import APIRouter
from api.v1.endpoints import chat

router = APIRouter()
router.include_router(chat.router)
