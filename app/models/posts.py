from datetime import datetime
from sqlalchemy import Column, Text, TIMESTAMP, ForeignKey, text, BigInteger
from sqlalchemy.orm import relationship

from app.database import Base


class Posts(Base):
    __tablename__ = "posts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
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

    tags = relationship("Tags", secondary="post_tags", back_populates="posts")

    metrics = relationship(
        "PostMetrics",
        cascade="all, delete-orphan",
        uselist=False,
        passive_deletes=True,
        back_populates="post",
    )
