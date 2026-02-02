from sqlalchemy import Column, Integer, ForeignKey, Text
from app.database import Base


class UserAuth(Base):
    __tablename__ = "user_auth"

    id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    password = Column(Text, nullable=False)
