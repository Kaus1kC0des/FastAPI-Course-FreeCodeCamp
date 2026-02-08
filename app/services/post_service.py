from app.models import Posts
from app.models.post_tags import PostTags
from app.models.tags import Tags
from app.models.post_metrics import PostMetrics
from app.schemas import PostUpdate, PostCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, update, insert
from sqlalchemy.orm import selectinload
import logging
import os

logger = logging.getLogger(__name__)


async def retrieve_total_posts(db: AsyncSession):
    try:
        query = select(func.count()).select_from(Posts)
        result = await db.scalar(query)
        return {"count": result}
    except Exception as e:
        raise e


def base_post_query():
    return (
        select(Posts)
        .join(PostMetrics, PostMetrics.post_id == Posts.id, isouter=True)
        .options(selectinload(Posts.author), selectinload(Posts.tags))
    )


def apply_post_filters(
    query, *, post_id: int | None, user_id: int | None, tag: str | None
):
    if post_id:
        query = query.where(Posts.id == post_id)

    if user_id:
        query = query.where(Posts.author_id == user_id)
    if tag:
        query = (
            query.join(PostTags, PostTags.post_id == Posts.id)
            .join(Tags, Tags.id == PostTags.tag_id)
            .distinct(Posts.id)
        )
    return query


def order_and_paginate(
    query, *, latest: bool | None, offset: int | None, limit: int | None
):
    if latest:
        return query.order_by(Posts.last_updated.desc()).limit(1)

    if offset:
        query = query.offset(offset)

    if limit:
        query = query.limit(int(os.getenv("DEFAULT_RETRIEVAL_LIMIT", 100)))
    return query


async def fetch_posts(
    db: AsyncSession,
    *,
    post_id: int | None = None,
    user_id: int | None = None,
    tag: str | None = None,
    latest: bool | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    try:
        query = base_post_query()
        query = apply_post_filters(query, post_id=post_id, user_id=user_id, tag=tag)
        query = order_and_paginate(query, latest=latest, offset=offset, limit=limit)
        results = await db.scalars(query)
        logger.info(f"Post with {post_id=} was returned")
        if post_id or latest:
            return results.first()
        return results.all()
    except Exception as e:
        logging.error(f"Error {e} occurred")
        raise e


async def update_post(id: int, post: PostUpdate, db: AsyncSession):
    try:
        query = (
            update(Posts)
            .where(Posts.id == id)
            .values(
                title=post.title or None,
                content=post.content or None,
            )
        )
        await db.execute(query, execution_options={"synchronize_session": False})
        await db.commit()
        return {"response": "Post Updated succesfully"}
    except Exception as e:
        await db.rollback()
        logger.error(f"Error {e} occurred")
        raise e


async def delete_post(id: int, db: AsyncSession):
    try:
        query = delete(Posts).where(Posts.id == id)
        await db.execute(query)
        await db.commit()
        logging.info(f"Post with {id=} has been deleted")
        return {"result": "Post Deleted Sucessfully"}
    except Exception as e:
        logger.error(f"Error {e} occurred")
        await db.rollback()
        raise e


async def create_post(post: PostCreate, db: AsyncSession):
    try:
        query = insert(Posts).returning(Posts.id)
        result = await db.scalar(query, [post.model_dump()])
        await db.commit()
        return {"result": "Insertion successful", "id": result}
    except Exception as e:
        logger.error(f"Error {e} occurred")
        await db.rollback()
        raise e
