from pydantic import Field, BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str

    model_config = ConfigDict(from_attributes=True)


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    tags: List[str]


class PostResponse(PostBase):
    id: int
    created_at: datetime


class PostTagSummary(BaseModel):
    id: int
    tag: str

    model_config = ConfigDict(from_attributes=True)


class PostAuthorSummary(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    image: Optional[str] = None
    role: Optional[str] = None
    email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PostListResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    last_updated: Optional[datetime] = None
    author_id: int
    tags: List[PostTagSummary] = []
    author: PostAuthorSummary
    is_bookmarked: bool = Field(default=False, alias="isBookmarked")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PostDetailResponse(PostBase):
    id: int
    created_at: datetime
    last_updated: Optional[datetime] = None
    author_id: int
    tags: List[PostTagSummary] = []
    author: PostAuthorSummary
    is_bookmarked: bool = Field(default=False, alias="isBookmarked")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
