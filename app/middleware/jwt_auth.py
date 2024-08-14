from http.client import HTTPException
import logging
import os
import jwt
from jwt.exceptions import PyJWTError
import requests
from starlette.authentication import (AuthenticationBackend, AuthenticationError)

logger = logging.getLogger(__name__)
class BearerAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        BASE_URL = os.getenv("BASE_URL",None)
        JWT_SECRET = os.getenv("JWT_SECRET",None)

        if not BASE_URL:
            raise HTTPException(status_code=401, detail="BASE_URL was not provided")
        if not JWT_SECRET:
            raise HTTPException(status_code=401, detail="JWT_SECRET was not provided")
        
        if "Authorization" not in conn.headers:
            raise AuthenticationError('Authorization token was not provided')

        auth = conn.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                raise AuthenticationError('Only Authorization Bearer Token is provided')
            decoded = jwt.decode(
                token,
                os.getenv("JWT_SECRET",None),
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
        except (ValueError, UnicodeDecodeError, PyJWTError) as exc:
            raise AuthenticationError('Invalid bearer auth credentials')
        userId: str = decoded.get("sub")
        # Get user from gateway
        response = requests.get(
            url=f"{BASE_URL}/api/users/{userId}",
            headers= {"Authorization": f"Bearer {token}"}
            )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid JWT token")
        user = response.json()
        if user is None:
            raise AuthenticationError('Invalid JWT Token.')
        return auth, user