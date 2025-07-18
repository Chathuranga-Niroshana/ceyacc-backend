from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserPreview(BaseModel):
    id: int
    name: str
    image: Optional[str]

    class Config:
        from_attributes = True

class QuizCreate(BaseModel):
    title: str
    question: str
    description: Optional[str] = None
    media_url_one: Optional[str] = None
    media_url_two: Optional[str] = None
    media_url_three: Optional[str] = None
    answer_one: str
    answer_two: str
    answer_three: Optional[str] = None
    answer_four: Optional[str] = None
    answer_five: Optional[str] = None
    correct_answer: int
    visibility: Optional[bool] = True

    class Config:
        from_attributes = True

class QuizResponse(QuizCreate):
    id: int
    user: UserPreview
    created_at: datetime

class QuizInteractionCreate(BaseModel):
    answer_id: int

    class Config:
        from_attributes = True

class QuizInteractionResponse(QuizInteractionCreate):
    id: int
    user: Optional[UserPreview] = None
    quiz_id: int
    created_at: datetime
