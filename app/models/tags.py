from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Tags(Base):
    __tablename__ = "tags"

    id = Column(
        Integer, primary_key=True, nullable=False, index=True, autoincrement=True
    )
    tag = Column(Text, unique=True, nullable=False)

    posts = relationship("Posts", secondary="post_tags", back_populates="tags")
