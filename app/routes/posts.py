import logging
import logging

from app.models.posts import Post
from fastapi import APIRouter, Depends, Query
from app.dependencies import get_db_async
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, func, delete, update
from app.schemas import PostCreate as PostModel
from app.schemas import PostUpdate

router = APIRouter()


@router.get("/posts/all", status_code=200)
async def get_all_posts(
    db: AsyncSession = Depends(get_db_async),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    try:
        query = select(Post).offset(offset).limit(limit).order_by(Post.id)
        results = await db.scalars(query)
        return {"posts": results.all(), "offset": offset, "limit": limit}
    except Exception as e:
        raise e


@router.get("/posts/latest")
async def get_latest_post(db: AsyncSession = Depends(get_db_async)):
    try:
        query = select(Post).order_by(Post.id).limit(1)
        result = await db.scalar(query)
        return {"post": result}
    except Exception as e:
        raise e


@router.get("/posts/total")
async def get_post_count(db: AsyncSession = Depends(get_db_async)):
    try:
        query = select(func.count()).select_from(Post)
        result = db.scalar(query)
        return {"count": result}
    except Exception as e:
        raise e


@router.get("/posts/{id}")
async def get_post_by_id(id: int, db: AsyncSession = Depends(get_db_async)):
    try:
        query = select(Post).where(Post.id == id)
        result = await db.scalar(query)
        return {"id": id, "post": result}
    except Exception as e:
        raise e


@router.post("/posts")
async def create_post(post: PostModel, db: AsyncSession = Depends(get_db_async)):
    try:
        query = insert(Post).returning(Post.id)
        result = await db.scalar(query, [post.model_dump()])
        await db.commit()
        logging.log(
            msg=f"post: {post} written into DB successfully", level=logging.INFO
        )
        return {"result": "Insertion successful", "id": result}
    except Exception as e:
        await db.rollback()
        raise e


@router.delete("/posts/{id}", status_code=204)
async def delete_post_by_id(id: int, db: AsyncSession = Depends(get_db_async)):
    try:
        query = delete(Post).where(Post.id == id)
        await db.execute(query)
        await db.commit()
        return {"result": "Post Deleted Sucessfully"}
    except Exception as e:
        await db.rollback()
        raise e


@router.put("/posts/{id}", status_code=200)
async def update_post_by_id(
    id: int, post: PostUpdate, db: AsyncSession = Depends(get_db_async)
):
    try:
        query = (
            update(Post)
            .where(Post.id == id)
            .values(
                title=post.title or None,
                content=post.content or None,
                published=post.published or None,
            )
        )
        await db.execute(query, execution_options={"synchronize_session": False})
        await db.commit()
        return {"response": "Post Updated succesfully"}
    except Exception as e:
        await db.rollback()
        raise e
