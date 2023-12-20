from fastapi import APIRouter
from app.api.notification import router as notificationRouter
from app.api.bulkNotification import router as bulkNotificationRouter

api = APIRouter()
api.include_router(notificationRouter)
api.include_router(bulkNotificationRouter)

__all__ = ["api"]