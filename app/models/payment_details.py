from sqlalchemy import ForeignKey
from sqlalchemy import Column, Text, DateTime, text, VARCHAR, Date, Integer, TEXT
from sqlalchemy.orm import relationship
from app.database import Base


class PaymentDetails(Base):
    __tablename__ = "payment_details"
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    card_expire = Column(Text)
    card_number = Column(Text)
    card_type = Column(Text)
    currency = Column(Text)
    iban = Column(Text)
