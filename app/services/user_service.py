from app.models.auth_details import UserAuth
from app.dependencies import get_db_async
from app.models import *
from app.schemas import *
from app.services.auth_service import hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete
from fastapi import Depends, HTTPException, status
from typing import Annotated


async def create_user(
    user: UserCreate, db: Annotated[AsyncSession, Depends(get_db_async)]
):
    try:
        data = user.model_dump(exclude={"confirm_password", "password"})
        password = hash(user.password)
        user_stmt = insert(Users).values(data).returning(Users.id)
        user_id = await db.scalar(user_stmt)
        auth_stmt = insert(UserAuth).values({"id": user_id, "password": password})
        await db.execute(auth_stmt)
        await db.commit()
        return {"result": "User Created Successfully!", "id": user_id}
    except Exception as e:
        await db.rollback()
        raise e


async def get_user(id: int, db: Annotated[AsyncSession, Depends(get_db_async)]):
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


async def delete_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db_async)]):
    try:
        stmt = delete(Users).where(Users.id == user_id)
        await db.scalar(stmt)
        await db.commit()
        return {"response": f"User with ID: {user_id} deleted"}
    except Exception as e:
        raise e
