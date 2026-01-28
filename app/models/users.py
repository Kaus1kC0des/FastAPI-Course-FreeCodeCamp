from datetime import datetime
from sqlalchemy import Column, Text, DateTime, text, VARCHAR, UUID
from sqlalchemy.orm import relationship

from app.database import Base
from uuid_utils import uuid7


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid7)
    first_name = Column(VARCHAR(255), nullable=False)
    last_name = Column(VARCHAR(255), nullable=False)
    email = Column(Text, unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now, server_default=text("NOW()"))
