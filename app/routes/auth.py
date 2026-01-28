from app.dependencies import get_db_async
from app.models.users import Users
from app.services.auth_service import (
    verify_password,
    create_access_token,
)
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter(prefix="/auth", tags=["Authentication", "User Management"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db_async)],
):
    try:
        stmt = select(Users).where(Users.email == user_credentials.username)
        user = await db.scalar(stmt)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exists"
            )

        if verify_password(user_credentials.password, str(user.password)):
            data = {"user_id": str(user.id), "role": "user"}
            token = create_access_token(data)
            return token
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Provided credentials are incorrect!",
            )
    except Exception as e:
        raise e
