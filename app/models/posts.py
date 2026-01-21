import asyncio
from datetime import datetime

from app.database import Base
from sqlalchemy import Column, BigInteger, Text, VARCHAR, Boolean, TIMESTAMP
from sqlalchemy import text


class Post(Base):
    __tablename__ = "posts"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    title = Column(VARCHAR(255), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=True, server_default=text("TRUE"))
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
        default=datetime.now,
    )
    last_updated = Column(TIMESTAMP(timezone=True), onupdate=datetime.now)

    def __str__(self):
        return f"""
                Post<id: {self.id} | title: {self.title} | content: {self.content} | published: {self.published} | created_at: {self.created_at} | updated_at: {self.last_updated}>
            """
