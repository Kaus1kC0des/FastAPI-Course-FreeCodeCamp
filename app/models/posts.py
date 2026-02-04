from datetime import datetime
from sqlalchemy import (
    Column,
    Text,
    TIMESTAMP,
    ForeignKey,
    text,
    Integer,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    content = Column(Text)

    author_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    author = relationship("Users", back_populates="posts")
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
        default=datetime.now,
    )
    last_updated = Column(TIMESTAMP(timezone=True), onupdate=datetime.now)

    tags = relationship("PostTags", uselist=True, cascade="all, delete-orphan")
