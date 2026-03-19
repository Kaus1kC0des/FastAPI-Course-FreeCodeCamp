from typing import Annotated
import logging
from fastapi import APIRouter, Depends, Query
from app.dependencies import get_db_async
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostListResponse,
    PostDetailResponse,
)
from app.services.auth_service import get_current_user
from app.services import post_service

router = APIRouter(
    prefix="/posts", tags=["Posts"], dependencies=[Depends(get_current_user)]
)


@router.get("/all", status_code=200, response_model=list[PostListResponse])
async def get_all_posts(
    user_id: Annotated[int, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db_async),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    result = await post_service.fetch_posts(
        db, viewer_user_id=user_id, offset=offset, limit=limit, no_content=True
    )
    return result


@router.get("/bookmarks", response_model=list[PostListResponse])
async def get_bookmarked_post_ids(
    user_id: Annotated[int, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db_async)],
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
):
    response = await post_service.retrieve_bookmarks(
        db, user_id, limit=limit, offset=offset
    )
    return response


@router.get("/latest", response_model=PostResponse)
async def get_latest_post(
    db: AsyncSession = Depends(get_db_async), user_id: int = Depends(get_current_user)
):
    result = await post_service.fetch_posts(db, latest=True)
    return result


@router.get("/total")
async def get_post_count(db: AsyncSession = Depends(get_db_async)):
    result = await post_service.retrieve_total_posts(db)
    return result


@router.get("/{post_id}", response_model=PostDetailResponse)
async def get_post_by_id(
    post_id: int,
    user_id: Annotated[int, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db_async),
):
    result = await post_service.fetch_posts(db, viewer_user_id=user_id, post_id=post_id)
    return result


@router.post("")
async def create_post(
    post: PostCreate,
    db: Annotated[AsyncSession, Depends(get_db_async)],
    user_id: Annotated[int, Depends(get_current_user)],
):
    post_id = await post_service.create_post(user_id, post, db)
    logging.info(f"User with {user_id=} created a new post with {post_id=}")
    return {"result": "New Post Created", "post_id": post_id}


@router.delete("/{id}", status_code=204)
async def delete_post_by_id(id: int, db: AsyncSession = Depends(get_db_async)):
    result = await post_service.delete_post(id, db)
    return result


@router.put("/{id}", status_code=200)
async def update_post_by_id(
    id: int, post: PostUpdate, db: Annotated[AsyncSession, Depends(get_db_async)]
):
    result = await post_service.update_post(id, post, db)
    return result


@router.get("/tags/{tag}", response_model=list[PostListResponse])
async def get_post_by_tag(
    tag: str,
    user_id: Annotated[int, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db_async)],
):
    response = await post_service.fetch_posts(
        db, tag=tag, viewer_user_id=user_id, no_content=True
    )
    return response


@router.post("/bookmark/{post_id}")
async def bookmark_post(
    user_id: Annotated[int, Depends(get_current_user)],
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db_async)],
):
    response = await post_service.bookmark_post(db, user_id, post_id)
    return response


@router.delete("/bookmark/{post_id}")
async def unbookmark_post(
    user_id: Annotated[int, Depends(get_current_user)],
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db_async)],
):
    response = await post_service.unbookmark_post(db, user_id, post_id)
    return response
