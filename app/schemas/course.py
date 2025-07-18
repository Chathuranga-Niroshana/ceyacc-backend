from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CourseAnswerCreate(BaseModel):
    answer: str

class CourseAnswerResponse(CourseAnswerCreate):
    id: int

    class Config:
        from_attributes = True

class CourseQuestionCreate(BaseModel):
    question: str
    answers: List[str]
    correct_answer: int = Field(..., alias="correctAnswer")
    marks: int

class CourseQuestionResponse(BaseModel):
    id: int
    question: str
    answers: List[str]
    correct_answer: int = Field(..., alias="correctAnswer")
    marks: int

    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    thumbnail: Optional[List[str]] = None
    media: Optional[List[str]] = None
    resources: Optional[List[str]] = None
    marks_for_pass: Optional[int] = Field(None, alias="marksForPass")
    applicable_grade: Optional[str] = Field(None, alias="applicableGrade")
    applicable_level: Optional[str] = Field(None, alias="applicableLevel")
    questions: List[CourseQuestionCreate]

    class Config:
        from_attributes = True
        allow_population_by_field_name = True

class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    thumbnail: Optional[List[str]] = None
    media: Optional[List[str]] = None
    resources: Optional[List[str]] = None
    marks_for_pass: Optional[int] = Field(None, alias="marksForPass")
    applicable_grade: Optional[str] = Field(None, alias="applicableGrade")
    applicable_level: Optional[str] = Field(None, alias="applicableLevel")
    questions: List[CourseQuestionResponse]
    created_at: datetime

    class Config:
        from_attributes = True
        allow_population_by_field_name = True
