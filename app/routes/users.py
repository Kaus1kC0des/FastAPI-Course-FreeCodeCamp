from app.schemas.user import UserCreate, UserResponse
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from fastapi import APIRouter, status, HTTPException
from app.models import Users
from app.dependencies import get_db_async
from app.services.auth_service import hash
from uuid import UUID
from typing import Annotated

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, db: Annotated[AsyncSession, Depends(get_db_async)]
):
    try:
        data = user.model_dump(exclude={"confirm_password"})
        data["password"] = hash(data["password"])
        stmt = insert(Users).values(data).returning(Users.id)
        result = await db.scalar(stmt)
        await db.commit()
        return {"result": "User Created Successfully!", "id": result}
    except Exception as e:
        await db.rollback()
        raise e


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(id: UUID, db: Annotated[AsyncSession, Depends(get_db_async)]):
    try:
        stmt = select(Users).where(Users.id == id)
        result = await db.scalar(stmt)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id = {id} not found",
            )
        return result
    except Exception as e:
        raise e
