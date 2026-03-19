from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import defer
from app.services import tag_service
from app.models import Posts, Bookmarks
from app.models.post_tags import PostTags
from app.models.tags import Tags
from app.models.post_metrics import PostMetrics
from app.schemas import PostUpdate, PostCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, update, and_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


async def retrieve_total_posts(db: AsyncSession):
    try:
        query = select(func.count()).select_from(Posts)
        result = await db.scalar(query)
        return {"count": result}
    except Exception as e:
        logger.error(f"Error {e} occurred")
        raise


def base_post_query(viewer_user_id: int | None = None, no_content: bool | None = False):
    options = [selectinload(Posts.author), selectinload(Posts.tags)]
    if no_content:
        options.append(defer(Posts.content))
    return (
        select(Posts, Bookmarks.post_id.is_not(None).label("is_bookmarked"))
        .join(PostMetrics, PostMetrics.post_id == Posts.id, isouter=True)
        .outerjoin(
            Bookmarks,
            and_(
                Bookmarks.post_id == Posts.id,
                Bookmarks.user_id == viewer_user_id,
            ),
        )
        .options(*options)
    )


def apply_post_filters(
    query, *, post_id: int | None, author_id: int | None, tag: str | None
):

    if post_id:
        query = query.where(Posts.id == post_id)

    if author_id:
        query = query.where(Posts.author_id == author_id)
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
    query = query.order_by(Posts.last_updated.desc())
    if latest:
        return query.limit(1)

    if offset:
        query = query.offset(offset)

    if limit:
        query = query.limit(limit)
    return query


async def fetch_posts(
    db: AsyncSession,
    viewer_user_id: int | None = None,
    *,
    author_id: int | None = None,
    post_id: int | None = None,
    tag: str | None = None,
    latest: bool | None = None,
    offset: int | None = None,
    limit: int | None = None,
    no_content: bool | None = False,
):
    try:
        query = base_post_query(viewer_user_id=viewer_user_id, no_content=no_content)
        query = apply_post_filters(query, post_id=post_id, author_id=author_id, tag=tag)
        query = order_and_paginate(query, latest=latest, offset=offset, limit=limit)
        results = await db.execute(query)

        if post_id or latest:
            row = results.first()
            if not row:
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
            post, is_bookmarked = row
            post.is_bookmarked = bool(is_bookmarked)
            return post

        rows = results.all()
        posts = []
        for post, is_bookmarked in rows:
            post.is_bookmarked = bool(is_bookmarked)
            posts.append(post)
        return posts
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


async def bookmark_post(db: AsyncSession, user_id: int, post_id: int):
    try:
        post = await fetch_posts(db, post_id=post_id)
        if not post:
            logger.error(
                f"User {user_id=} tried to bookmark a post with {post_id=} that does not exists!"
            )
            return {"result": f"Post with {post_id=} does not exists!"}
        stmt = (
            insert(Bookmarks)
            .values(post_id=post_id, user_id=user_id)
            .on_conflict_do_nothing()
        )
        await db.execute(stmt)
        await db.commit()
        logger.info(f"User {user_id} bookmarked Post {post_id}")
        return {"response": f"Post '{post_id=}' bookmarked"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error {e} occurred")
        await db.rollback()
        raise


async def retrieve_bookmarks(
    db: AsyncSession, user_id: int, limit: int | None, offset: int | None
):
    try:
        stmt = (
            select(Posts, Bookmarks.post_id.is_not(None).label("is_bookmarked"))
            .join(Bookmarks, Bookmarks.post_id == Posts.id)
            .where(Bookmarks.user_id == user_id)
            .options(
                selectinload(Posts.author),
                selectinload(Posts.tags),
                defer(Posts.content),
            )
        )
        stmt = order_and_paginate(stmt, latest=False, limit=limit, offset=offset)
        result = await db.execute(stmt)
        rows = result.all()
        posts = []
        for post, is_bookmarked in rows:
            post.is_bookmarked = bool(is_bookmarked)
            posts.append(post)
        return posts

    except Exception as e:
        logger.error(f"Error {e} occurred")
        raise


async def unbookmark_post(db: AsyncSession, user_id: int, post_id: int):
    try:
        stmt = delete(Bookmarks).where(
            Bookmarks.user_id == user_id, Bookmarks.post_id == post_id
        )
        result = await db.execute(stmt)
        await db.commit()
        if result.rowcount == 0:
            return {"response": "Bookmark not found"}
        return {"response": "Bookmark removed"}
    except Exception as e:
        logger.error(f"Error {e} occurred")
        await db.rollback()
        raise
