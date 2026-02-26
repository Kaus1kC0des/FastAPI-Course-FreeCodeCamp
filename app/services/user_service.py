from app.models import *
from app.schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


async def create_user(data: dict, db: AsyncSession):
    try:
        new_user = Users(
            clerk_user_id=data["id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email_addresses"][0]["email_address"],
            user_name=data.get("username") or data["id"],
            image=data.get("image_url"),
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info(f"User with clerk_user_id={new_user.clerk_user_id} created")
        return {"result": "User Created Successfully!", "id": new_user.id}
    except Exception as e:
        logger.error(f"Error {e} occurred")
        await db.rollback()
        raise


async def get_user(id: int, db: AsyncSession):
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
        logging.error(f"Error {e} occurred")
        raise


async def delete_user(user_id: int, db: AsyncSession):
    try:
        stmt = delete(Users).where(Users.id == user_id)
        await db.scalar(stmt)
        await db.commit()
        logging.info(f"User with {user_id=} deleted")
        return {"response": f"User with ID: {user_id} deleted"}
    except Exception as e:
        await db.rollback()
        raise
