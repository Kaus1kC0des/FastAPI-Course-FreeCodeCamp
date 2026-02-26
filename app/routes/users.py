import os
from app.services.auth_service import get_current_user
from app.schemas.user import UserResponse
from app.dependencies import get_db_async
from app.services import user_service
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Request
from svix.webhooks import Webhook
from typing import Annotated

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user_route(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db_async)],
):
    body = await request.body()
    svix_headers = {
        "svix-id": request.headers.get("svix-id", ""),
        "svix-timestamp": request.headers.get("svix-timestamp", ""),
        "svix-signature": request.headers.get("svix-signature", ""),
    }
    wh = Webhook(os.getenv("CLERK_SIGNING_SECRET", ""))
    payload = wh.verify(data=body, headers=svix_headers)

    if payload["type"] == "user.created":
        result = await user_service.create_user(payload["data"], db)
        return result

    return {"result": "Event ignored"}


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
