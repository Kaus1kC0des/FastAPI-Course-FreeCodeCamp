from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class PostMetrics(Base):
    __tablename__ = "post_metrics"

    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    likes = Column(Integer, nullable=False, default=0)
    dislikes = Column(Integer, nullable=False, default=0)
    views = Column(Integer, nullable=False, default=0)

    post = relationship(
        "Posts",
        back_populates="metrics",
    )
