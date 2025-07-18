from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserPreview(BaseModel):
    id: int
    name: str
    image: Optional[str]

    class Config:
        from_attributes = True

class ExamPaperCreate(BaseModel):
    subject: str
    grade: int
    school: str
    semester: str
    year: str
    exam_type: Optional[str] = Field(None, alias="examType")
    description: Optional[str] = None
    media: Optional[List[str]] = None

    class Config:
        from_attributes = True
        allow_population_by_field_name = True

class ExamPaperUpdate(BaseModel):
    subject: Optional[str] = None
    grade: Optional[int] = None
    school: Optional[str] = None
    semester: Optional[str] = None
    year: Optional[str] = None
    exam_type: Optional[str] = Field(None, alias="examType")
    description: Optional[str] = None
    media: Optional[List[str]] = None

    class Config:
        from_attributes = True
        allow_population_by_field_name = True

class ExamPaperResponse(ExamPaperCreate):
    id: int
    created_at: datetime
    # Optionally, add user: UserPreview if you want to show who uploaded the paper
