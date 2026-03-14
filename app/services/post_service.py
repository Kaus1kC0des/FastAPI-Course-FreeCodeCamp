from typing import List
from sqlalchemy.orm import defer
from app.services import tag_service
from app.models import Posts
from app.models.post_tags import PostTags
from app.models.tags import Tags
from app.models.post_metrics import PostMetrics
from app.schemas import PostUpdate, PostCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, update
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
import logging
import os

logger = logging.getLogger(__name__)


async def retrieve_total_posts(db: AsyncSession):
    try:
        query = select(func.count()).select_from(Posts)
        result = await db.scalar(query)
        return {"count": result}
    except Exception as e:
        logger.error(f"Error {e} occurred")
        raise


def base_post_query(no_content: bool | None = False):
    options = [selectinload(Posts.author), selectinload(Posts.tags)]
    if no_content:
        options.append(defer(Posts.content))
    return (
        select(Posts)
        .join(PostMetrics, PostMetrics.post_id == Posts.id, isouter=True)
        .options(*options)
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
            .where(Tags.tag == tag)
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
    no_content: bool | None = False,
):
    try:
        query = base_post_query(no_content=no_content)
        query = apply_post_filters(query, post_id=post_id, user_id=user_id, tag=tag)
        query = order_and_paginate(query, latest=latest, offset=offset, limit=limit)
        results = await db.scalars(query)

        if post_id or latest:
            result = results.first()
            if not result:
                if post_id:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id = {post_id} not found",
                    )
                else:  # latest
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No posts available",
                    )
            logger.info(f"Post with {post_id=} was returned")
            return result
        return results.all()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error {e} occurred")
        raise


async def update_post(post_id: int, post: PostUpdate, db: AsyncSession):
    try:
        query = (
            update(Posts)
            .where(Posts.id == post_id)
            .values(
                title=post.title or None,
                content=post.content or None,
            )
        )
        await db.execute(query, execution_options={"synchronize_session": False})
        await db.commit()
        return {"response": "Post Updated successfully"}
    except Exception as e:
        await db.rollback()
        logger.error(f"Error {e} occurred")
        raise


async def delete_post(post_id: int, db: AsyncSession):
    try:
        query = delete(Posts).where(Posts.id == post_id)
        await db.execute(query)
        await db.commit()
        logging.info(f"Post with {id=} has been deleted")
        return {"result": "Post Deleted Successfully"}
    except Exception as e:
        logger.error(f"Error {e} occurred")
        await db.rollback()
        raise


async def create_post(user_id: int, post: PostCreate, db: AsyncSession):
    try:
        new_post = Posts(**post.model_dump(exclude={"tags"}), author_id=user_id)
        db.add(new_post)
        await db.flush()
        for tag_name in post.tags:
            tag = await tag_service.get_or_create_tag(db, tag_name)
            db.add(PostTags(post_id=new_post.id, tag_id=tag.id))
        await db.commit()
        logger.info(f"Post with {new_post.id} created by {user_id}")
        return {"id": new_post.id}
    except Exception as e:
        await db.rollback()
        logger.error(f"Error {e} occurred")
        raise
