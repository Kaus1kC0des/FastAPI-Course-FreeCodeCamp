from pydantic import Field
from typing import List
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    author_id: int = Field(alias="userId")
    tags: List[str]


class DummyPostCreate(BaseModel):
    title: str
    content: str = Field(alias="body")
    tags: list[str]
    reactions: dict
    views: int
    author_id: int = Field(alias="userId")


class PostResponse(PostBase):
    id: int
    created_at: datetime
