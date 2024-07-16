from fastapi import APIRouter
from .payments import router as clientbot_api_router

api_router = APIRouter()
api_router.include_router(clientbot_api_router, prefix="/test")
