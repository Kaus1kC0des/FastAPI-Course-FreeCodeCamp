from sqlalchemy import Column, Text, BigInteger, ForeignKey, TIMESTAMP, text
import datetime
from app.database import Base


class Comments(Base):

    __tablename__ = "comments"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    post_id = Column(
        BigInteger,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    comment = Column(Text, nullable=False)

    parent_comment_id = Column(
        BigInteger,
        ForeignKey("comments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
        default=datetime.datetime.now,
    )
    last_updated = Column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )
