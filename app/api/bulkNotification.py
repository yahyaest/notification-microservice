import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.prisma import prisma

logger = logging.getLogger(__name__)
router = APIRouter()

class Notification(BaseModel):
    userEmail: Optional[str] = None
    userId: Optional[int] = None
    username: str
    userImage: Optional[str] = None
    title: str
    message: str
    sender : Optional[str] = None
    seen: Optional[bool] = False

@router.patch("/bulk_notifications", tags=["notification"])
async def update_bulk_notification(body: dict, request: Request):
    try:
        user = request.user

        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        notifications = await prisma.notification.find_many(
            where= { 'userEmail': user.get('email') }
        )

        if not notifications:
            raise HTTPException(status_code=404, detail="Notifications not found")
        
        if user.get('email') != notifications[0].userEmail and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Notifications belong to another user")    

        updatedNotifications = await prisma.notification.update_many(
            where= { 'userEmail': user.get('email') },
            data= dict(body)
        )

        return updatedNotifications
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=e.detail)