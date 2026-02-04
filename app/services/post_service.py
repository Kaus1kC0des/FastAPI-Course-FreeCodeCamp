from app.models.post_tags import PostTags
from app.models.tags import Tags
from app.models.post_metrics import PostMetrics
from app.dependencies import get_db_async
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def retrieve_posts(
    db: AsyncSession = Depends(get_db_async),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    try:
        query = select(Posts).offset(offset).limit(limit).order_by(Posts.id)
        results = await db.scalars(query)
        return {"posts": results.all(), "offset": offset, "limit": limit}
    except Exception as e:
        raise e


async def retrieve_latest_post(db: AsyncSession = Depends(get_db_async)):
    try:
        query = select(Posts).order_by(Posts.id.desc()).limit(1)
        result = await db.scalar(query)
        result.id = str(result.id)
        return result
    except Exception as e:
        raise e


async def retrieve_total_posts(db: AsyncSession = Depends(get_db_async)):
    try:
        query = select(func.count()).select_from(Posts)
        result = db.scalar(query)
        return {"count": result}
    except Exception as e:
        raise e


async def retrieve_post_by_id(id: int, db: AsyncSession = Depends(get_db_async)):
    try:
        query = select(Posts).where(Posts.id == id)
        result = await db.scalar(query)
        print(result)
        return result
    except Exception as e:
        raise e
