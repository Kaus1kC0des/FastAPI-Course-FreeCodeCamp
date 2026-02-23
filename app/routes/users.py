from app.services.auth_service import get_current_user
from app.schemas.user import UserCreate, UserResponse
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status
from app.dependencies import get_db_async
from app.services import user_service
from typing import Annotated

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user_route(
    user: UserCreate, db: Annotated[AsyncSession, Depends(get_db_async)]
):
    result = await user_service.create_user(user, db)
    return result


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_route(id: int, db: Annotated[AsyncSession, Depends(get_db_async)]):
    result = await user_service.get_user(id, db)
    return result


@router.delete("/delete")
async def delete_user(
    user_id: Annotated[int, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db_async)],
):
    result = await user_service.delete_user(user_id, db)
    return result
