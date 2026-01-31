from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy import Column, Text, DateTime, text, VARCHAR, Date, Integer, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from app.database import Base
from app.models.enums import GenderEnum


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(VARCHAR(255), nullable=False)
    last_name = Column(VARCHAR(255), nullable=False)
    age = Column(Integer)
    gender = Column(ENUM(GenderEnum, name="gender_enum", create_type=True))
    email = Column(Text, unique=True, nullable=False, index=True)
    phone = Column(Text)
    user_name = Column(VARCHAR(128), nullable=False)
    birth_date = Column(Date)
    image = Column(TEXT)
    ein = Column(VARCHAR(20), nullable=False)
    ssn = Column(VARCHAR(25), nullable=False, unique=True)
    role = Column(VARCHAR(20))
    address = relationship(
        "Address", uselist=False, cascade="all, delete-orphan", passive_deletes=True
    )

    company_id = Column(ForeignKey("company_details.id"))

    created_at = Column(DateTime, default=datetime.now, server_default=text("NOW()"))
    posts = relationship(
        "Posts",
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
