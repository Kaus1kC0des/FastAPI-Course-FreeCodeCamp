from datetime import datetime
from sqlalchemy import Column, UUID, Text, VARCHAR, Boolean, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship

from app.database import Base
from uuid_utils import uuid7


class Posts(Base):
    __tablename__ = "posts"

    id = Column(UUID, primary_key=True, index=True, default=uuid7)
    title = Column(VARCHAR(255), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=True, server_default=text("true"))

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
        default=datetime.now,
    )
    last_updated = Column(TIMESTAMP(timezone=True), onupdate=datetime.now)
