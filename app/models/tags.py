from sqlalchemy import Column, Integer, ForeignKey, Text
from app.database import Base


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    tag = Column(Text, unique=True, nullable=False)
