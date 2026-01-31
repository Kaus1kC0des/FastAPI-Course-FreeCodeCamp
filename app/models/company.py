from sqlalchemy import ForeignKey
from sqlalchemy import Column, Text, DateTime, text, VARCHAR, Date, Integer, TEXT
from sqlalchemy.orm import relationship
from app.database import Base


class Company(Base):
    __tablename__ = "company_details"
    id = Column(Integer, autoincrement=True, primary_key=True)
    company_name = Column(Text)
    department = Column(Text)
    title = Column(Text)
    address = relationship(
        "CompanyAddress",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
