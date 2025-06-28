from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserPreview(BaseModel):
    id: int
    name: str
    image: Optional[str]

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    comment: str
    post_id: int
    parent_comment_id: Optional[int] = None

    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    id: int
    comment: str
    created_at: datetime
    updated_at: datetime
    user: UserPreview
    parent_comment_id: Optional[int] = None
    replies: Optional[List["CommentResponse"]] = []  # recursive replies

    class Config:
        from_attributes = True


CommentResponse.update_forward_refs()


class ReactionCreate(BaseModel):
    reaction_type_id: int
    post_id: int


class ReactionResponse(BaseModel):
    id: int
    reaction_type_id: int
    created_at: datetime
    user: UserPreview

    class Config:
        from_attributes = True


class RatingResponse(BaseModel):
    id: int
    type: str
    ratings: float
    user: UserPreview
    created_at: datetime

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    media_link: Optional[str] = None
    media_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = True


class PostResponse(PostCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    user: UserPreview
    comments: List[CommentResponse] = []
    reactions: List[ReactionResponse] = []
    ratings: List[RatingResponse] = []

    comments_number: int
    reaction_number: int
    post_ratings: float

    class Config:
        from_attributes = True
