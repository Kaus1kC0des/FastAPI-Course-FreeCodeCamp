from sqlalchemy import ForeignKey
from sqlalchemy import Column, Text, Integer
from app.database import Base


class CompanyAddress(Base):
    __tablename__ = "company_address"

    company_id = Column(ForeignKey("company_details.id"), primary_key=True, unique=True)
    address = Column(Text)
    city = Column(Text)
    state = Column(Text)
    state_code = Column(Text)
    postal_code = Column(Integer)
    country = Column(Text)
