import email
from sqlalchemy import Column, Text, VARCHAR, Date, Integer, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from app.database import Base
from app.models.enums import GenderEnum


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(255), nullable=False)
    last_name = Column(VARCHAR(255), nullable=False)
    age = Column(Integer)
    gender = Column(ENUM(GenderEnum, name="gender_enum"))
    phone = Column(Text)
    email = Column(Text, nullable=False, unique=True)
    user_name = Column(VARCHAR(128), nullable=False)
    birth_date = Column(Date)
    image = Column(TEXT)
    role = Column(VARCHAR(20))

    auth = relationship(
        "UserAuth", cascade="all, delete-orphan", uselist=False, passive_deletes=True
    )
    posts = relationship("Posts", cascade="all, delete-orphan", back_populates="author")
