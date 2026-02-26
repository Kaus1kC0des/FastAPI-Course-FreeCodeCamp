import os
import logging
import jwt
from jwt import PyJWKClient
from typing import Annotated
from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.dependencies import get_db_async

logger = logging.getLogger(__name__)

CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL", "")
jwks_client = PyJWKClient(CLERK_JWKS_URL)
bearer_scheme = HTTPBearer()


def verify_clerk_token(token: str) -> str:
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(token, signing_key.key, algorithms=["RS256"])
        clerk_user_id = payload.get("sub")
        if not clerk_user_id:
            raise ValueError("No sub claim in token")
        return clerk_user_id
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: Annotated[AsyncSession, Depends(get_db_async)],
) -> int:
    from app.models.users import Users

    clerk_user_id = verify_clerk_token(credentials.credentials)

    stmt = select(Users.id).where(Users.clerk_user_id == clerk_user_id)
    user_id = await db.scalar(stmt)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please register.",
        )
    return user_id
