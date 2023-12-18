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
    seen: Optional[bool] = False


@router.get("/notifications", tags=["notification"])
async def get_notifications(request: Request):
    try:
        user = request.user
        params = request.query_params
        query_dict = dict(params)

        if user and user.get("role") != 'ADMIN':
            query_dict["userEmail"] = user.get('email')

        if not query_dict:
            notification = await prisma.notification.find_many()
        else:
            if(params.get("id")):
                query_dict["id"] = int(query_dict["id"])

            if(params.get("userId")):
                query_dict["userId"] = int(query_dict["userId"])

            notification = await prisma.notification.find_many(
                where=query_dict,
            )
        return notification

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Notifications not found")

@router.get("/notifications/{notification_id}", tags=["notification"])
async def get_notification(notification_id : int, request: Request):
    try:
        user = request.user
        notification = await prisma.notification.find_unique(where={'id':notification_id })

        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        if user.get('email') != notification.userEmail and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Notification belong to another user")      

        return notification
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=e.detail)

@router.post("/notifications", tags=["notification"])
async def add_notification(body: Notification):
    try:
        notification = await prisma.notification.create(
            {
                "userEmail": body.userEmail,
                "username": body.username,
                "userImage": body.userImage,
                "userId": body.userId,
                "title": body.title,
                "message": body.message,
                "seen": body.seen,
            }
        )
        return notification
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Failed to post notification")

@router.patch("/notifications/{notification_id}", tags=["notification"])
async def update_notification(notification_id:int, body: dict, request: Request):
    try:
        user = request.user
        notification = await prisma.notification.find_unique(where={'id': notification_id })

        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        if user.get('email') != notification.userEmail and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Notification belong to another user")    

        notification = await prisma.notification.update(
            where= { 'id': notification_id },
            data= dict(body)
        )

        return notification
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=e.detail)

@router.delete("/notifications/{notification_id}", tags=["notification"])
async def delete_notification(notification_id:int, request: Request):
    try:
        user = request.user
        notification = await prisma.notification.find_unique(where={'id': notification_id })

        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        if user.get('email') != notification.userEmail and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Notification belong to another user")

        notification = await prisma.notification.delete(
            where= { 'id': notification_id }
        )

        return notification
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=e.detail)