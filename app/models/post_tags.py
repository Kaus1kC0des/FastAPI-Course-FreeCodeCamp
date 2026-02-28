from sqlalchemy import Column, BigInteger, ForeignKey, Integer
from app.database import Base


class PostTags(Base):
    __tablename__ = "post_tags"

    post_id = Column(
        BigInteger,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True, nullable=False)
