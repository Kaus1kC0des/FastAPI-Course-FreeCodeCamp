from datetime import datetime
from sqlalchemy import (
    Column,
    Text,
    VARCHAR,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    text,
    Integer,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=True, server_default=text("true"))
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
        default=datetime.now,
    )
    last_updated = Column(TIMESTAMP(timezone=True), onupdate=datetime.now)
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    author = relationship(
        "Users",
        back_populates="posts",
    )
