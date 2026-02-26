from sqlalchemy import Column, Text, VARCHAR, Date, Integer, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(255), nullable=False)
    last_name = Column(VARCHAR(255), nullable=False)
    phone = Column(Text)
    email = Column(Text, nullable=False, unique=True)
    username = Column(VARCHAR(128), nullable=False)
    image = Column(TEXT)
    role = Column(VARCHAR(20), default="user")
    clerk_user_id = Column(VARCHAR(255), nullable=True, unique=True, index=True)

    posts = relationship("Posts", cascade="all, delete-orphan", back_populates="author")
