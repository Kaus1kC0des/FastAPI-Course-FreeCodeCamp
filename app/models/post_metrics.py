from sqlalchemy import Column, ForeignKey, BigInteger
from app.database import Base
from sqlalchemy.orm import relationship


class PostMetrics(Base):
    __tablename__ = "post_metrics"

    post_id = Column(BigInteger, ForeignKey("posts.id"), primary_key=True)
    likes = Column(BigInteger, nullable=False, default=0)
    dislikes = Column(BigInteger, nullable=False, default=0)
    views = Column(BigInteger, nullable=False, default=0)

    post = relationship(
        "Posts",
        back_populates="metrics",
    )
