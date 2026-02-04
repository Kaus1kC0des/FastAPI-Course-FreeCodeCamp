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
    try:
        result = await post_service.retrieve_posts(db, offset, limit)
        return result
    except Exception as e:
        raise e


@router.get("/latest", response_model=PostResponse)
async def get_latest_post(db: AsyncSession = Depends(get_db_async)):
    try:
        result = await post_service.retrieve_latest_post(db)
        return result
    except Exception as e:
        raise e


@router.get("/total")
async def get_post_count(db: AsyncSession = Depends(get_db_async)):
    try:
        result = await post_service.retrieve_total_posts(db)
        return {"count": result}
    except Exception as e:
        raise e


@router.get("/{id}", response_model=PostResponse)
async def get_post_by_id(id: int, db: AsyncSession = Depends(get_db_async)):
    try:
        result = await post_service.retrieve_post_by_id(id, db)
        return result
    except Exception as e:
        raise e


@router.post("")
async def create_post(
    post: PostCreate,
    db: Annotated[AsyncSession, Depends(get_db_async)],
    user_id: Annotated[int, Depends(get_current_user)],
):
    try:
        print(f"{user_id=}")
        print(f"{type(user_id)=}")
        query = insert(Posts).returning(Posts.id)
        result = await db.scalar(query, [post.model_dump()])
        await db.commit()
        logging.log(
            msg=f"post: {post} written into DB successfully", level=logging.INFO
        )
        return {"result": "Insertion successful", "id": result}
    except Exception as e:
        await db.rollback()
        raise e


@router.delete("/{id}", status_code=204)
async def delete_post_by_id(id: int, db: AsyncSession = Depends(get_db_async)):
    try:
        query = delete(Posts).where(Posts.id == id)
        await db.execute(query)
        await db.commit()
        return {"result": "Post Deleted Sucessfully"}
    except Exception as e:
        await db.rollback()
        raise e


@router.put("/{id}", status_code=200)
async def update_post_by_id(
    id: int, post: PostUpdate, db: AsyncSession = Depends(get_db_async)
):
    try:
        query = (
            update(Posts)
            .where(Posts.id == id)
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
