from sqlalchemy import Column, BigInteger, ForeignKey
from app.database import Base


class BookMarks(Base):
    __tablename__ = "bookmarks"

    post_id = Column(
        BigInteger,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    user_id = Column(
        BigInteger, ForeignKey("users.id"), primary_key=True, nullable=False
    )
