from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserPreview(BaseModel):
    id: int
    name: str
    image: Optional[str]

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    title: str
    date_time: datetime
    location: str
    description: str
    media_url_one: Optional[str] = None
    media_url_two: Optional[str] = None
    media_url_three: Optional[str] = None
    media_url_four: Optional[str] = None
    media_url_five: Optional[str] = None

    class Config:
        from_attributes = True


class EventResponse(EventCreate):
    user: UserPreview
    id: int
    created_at: datetime


class EventInterestsCreate(BaseModel):
    interest_type: str

    class Config:
        from_attributes = True


class EventInterestResponse(EventInterestsCreate):
    id: int
    user: Optional[UserPreview] = None
    created_at: datetime
