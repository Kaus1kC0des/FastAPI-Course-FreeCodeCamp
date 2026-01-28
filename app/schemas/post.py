from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: UUID
    created_at: datetime
