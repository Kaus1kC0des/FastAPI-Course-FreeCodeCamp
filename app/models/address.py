from sqlalchemy import ForeignKey
from sqlalchemy import Column, Text, DateTime, text, VARCHAR, Date, Integer, TEXT
from sqlalchemy.orm import relationship
from app.database import Base


class Address(Base):
    __tablename__ = "address"
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    company_id = Column(ForeignKey("users.id"), primary_key=True)
    address = Column(Text)
    city = Column(Text)
    state = Column(Text)
    state_code = Column(Text)
    postal_code = Column(Integer)
    country = Column(Text)
