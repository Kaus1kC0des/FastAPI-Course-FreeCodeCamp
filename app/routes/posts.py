import logging
from app.models.post_metrics import PostMetrics
from app.models.post_tags import PostTags
from app.models.tags import Tags
from app.schemas import DummyPostCreate
from typing import Annotated
import logging
from app.models.posts import Posts
from fastapi import APIRouter, Depends, Query
from app.dependencies import get_db_async
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, func, delete, update
from app.schemas import PostCreate, PostUpdate, PostResponse
from app.services.auth_service import get_current_user
from app.services import post_service

router = APIRouter(
    prefix="/posts", tags=["Posts"], dependencies=[Depends(get_current_user)]
)


@router.get("/all", status_code=200)
async def get_all_posts(
    db: AsyncSession = Depends(get_db_async),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    result = await post_service.fetch_posts(db, offset=offset, limit=limit)
    return result


@router.get("/latest", response_model=PostResponse)
async def get_latest_post(db: AsyncSession = Depends(get_db_async)):
    result = await post_service.fetch_posts(db, latest=True)
    return result


@router.get("/total")
async def get_post_count(db: AsyncSession = Depends(get_db_async)):
    result = await post_service.retrieve_total_posts(db)
    return result


@router.get("/{post_id}", response_model=PostResponse)
async def get_post_by_id(post_id: int, db: AsyncSession = Depends(get_db_async)):
    result = await post_service.fetch_posts(db, post_id=post_id)
    return result


@router.post("")
async def create_post(
    post: PostCreate,
    db: Annotated[AsyncSession, Depends(get_db_async)],
    user_id: Annotated[int, Depends(get_current_user)],
):
    result = await post_service.create_post(post, db)
    logging.info(f"User with {user_id=} has created a post")
    return result


@router.delete("/{id}", status_code=204)
async def delete_post_by_id(id: int, db: AsyncSession = Depends(get_db_async)):
    result = await post_service.delete_post(id, db)
    return result


@router.put("/{id}", status_code=200)
async def update_post_by_id(
    id: int, post: PostUpdate, db: AsyncSession = Depends(get_db_async)
):
    result = await post_service.update_post(id, post, db)
    return result


@router.post("/ingest")
async def create_dummy_post(
    post: DummyPostCreate, db: AsyncSession = Depends(get_db_async)
):
    async with db.begin():
        new_post = Posts(
            title=post.title,
            content=post.content,
            author_id=post.author_id,
        )
        db.add(new_post)
        await db.flush()

        tag_objects = []

        for tag_name in post.tags:
            tag = await db.scalar(select(Tags).where(Tags.tag == tag_name))
            if not tag:
                tag = Tags(tag=tag_name)
                db.add(tag)
                await db.flush()
            tag_objects.append(tag)

        for tag in tag_objects:
            db.add(PostTags(post_id=new_post.id, tag_id=tag.id))

        metrics = PostMetrics(
            post_id=new_post.id,
            likes=post.reactions.get("likes", 0),
            dislikes=post.reactions.get("dislikes", 0),
            views=post.views,
        )
        db.add(metrics)
