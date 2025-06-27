from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ----------------------------------------
# Basic User Info (minimal for responses)
# ----------------------------------------
class UserPreview(BaseModel):
    id: int
    name: str
    image: Optional[str]

    class Config:
        orm_mode = True


# ----------------------------------------
# Comment Model (with recursive replies)
# ----------------------------------------
class CommentResponse(BaseModel):
    id: int
    comment: str
    created_at: datetime
    updated_at: datetime
    user: UserPreview
    parent_comment_id: Optional[int] = None
    replies: Optional[List["CommentResponse"]] = []  # recursive replies

    class Config:
        orm_mode = True


# Required for recursive model
CommentResponse.update_forward_refs()


# ----------------------------------------
# Reaction Model
# ----------------------------------------
class ReactionResponse(BaseModel):
    id: int
    reaction_type_id: int
    created_at: datetime
    user: UserPreview

    class Config:
        orm_mode = True


class RatingResponse(BaseModel):
    id: int
    type: str
    ratings: float
    user: UserPreview
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    id: int
    media_link: Optional[str] = None
    media_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = True
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
        orm_mode = True
