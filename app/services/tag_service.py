from app.models.tags import Tags
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
import logging

logger = logging.getLogger(__name__)


async def get_or_create_tag(db: AsyncSession, tag: str):
    try:
        stmt = (
            insert(Tags)
            .values(tag=tag)
            .on_conflict_do_update(index_elements=["tag"], set_={"tag": tag})
            .returning(Tags)
        )
        result = await db.execute(stmt)
        out = result.scalars().first()
        return out
    except Exception as e:
        logger.error(e)
