from fastapi import APIRouter
from app.api.notification import router as notificationRouter

api = APIRouter()
api.include_router(notificationRouter)

__all__ = ["api"]