import logging
import os
from fastapi import HTTPException, Request, Response
import requests
import jwt

logger = logging.getLogger(__name__)

# Middleware to intercept and validate JWT token
async def auth_middleware(request: Request, call_next):
    try:
        GATEWAY_BASE_URL = os.getenv("GATEWAY_BASE_URL",None)
        JWT_SECRET = os.getenv("JWT_SECRET",None)

        if not GATEWAY_BASE_URL:
            raise HTTPException(status_code=401, detail="GATEWAY_BASE_URL was not provided")
        if not JWT_SECRET:
            raise HTTPException(status_code=401, detail="JWT_SECRET was not provided")
                        
        token = request.headers.get("authorization").replace('Bearer ', '')
        logger.info("token is : ", token)
        if not token:
            raise HTTPException(status_code=401, detail="JWT token not found")

        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_mail = payload.get("email")
        if not user_mail:
            raise HTTPException(status_code=401, detail="Email not found in token")
        
        response = requests.post(
            url=f"{GATEWAY_BASE_URL}/api/users/is_user", 
            data={ "email": user_mail }, 
            headers= {"Authorization": f"Bearer {token}"}
            )
        
        if response.status_code != 201:
            raise HTTPException(status_code=401, detail="Invalid JWT token")
        response = response.json()

        if not response:
            raise HTTPException(status_code=401, detail="Invalid User")

        response = await call_next(request)
        return response
    except Exception as error:
        logger.error(error)
        return Response(content=str(error), status_code=401, media_type="application/json")
