from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class SexEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class TeachingExperienceEnum(str, Enum):
    BEGINNER = "0-1 Years"
    INTERMEDIATE = "1-4 Years"
    EXPERIENCED = "4-10 Years"
    MASTER = "10+ Years"


class UserBase(BaseModel):
    image: Optional[str] = None
    cover_image: Optional[str] = None
    name: str
    bio: Optional[str] = None
    email: EmailStr
    mobile_no: Optional[str] = None
    dob: Optional[datetime] = None
    system_score: Optional[float] = 10.0
    school_name: Optional[str] = None
    address_line_one: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    sex: Optional[SexEnum] = None
    nic: Optional[str] = None
    is_verified: Optional[bool] = True
    role_id: Optional[int] = 1


class UserCreate(UserBase):
    password: str


class TeacherCreate(BaseModel):
    subjects_taught: List[str]
    teaching_experience: Optional[TeachingExperienceEnum] = None


class StudentCreate(BaseModel):
    grade: int = Field(default=1, ge=1, le=13)


class UserFullCreate(UserCreate):
    teacher: Optional[TeacherCreate] = None
    student: Optional[StudentCreate] = None


class UserUpdate(BaseModel):
    image: Optional[str] = None
    cover_image: Optional[str] = None
    name: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    mobile_no: Optional[str] = None
    dob: Optional[datetime] = None
    # system_score: Optional[float] = None
    school_name: Optional[str] = None
    address_line_one: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    sex: Optional[SexEnum] = None
    nic: Optional[str] = None
    is_verified: Optional[bool] = None
    role_id: Optional[int] = None


class Teacher(BaseModel):
    id: int
    subjects_taught: List[str]
    teaching_experience: Optional[TeachingExperienceEnum] = None

    class Config:
        from_attributes = True


class Student(BaseModel):
    id: int
    grade: int
    is_completed: bool

    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    teacher: Optional[Teacher] = None
    student: Optional[Student] = None

    class Config:
        from_attributes = True


class ScoreLevel(BaseModel):
    id: int
    name: str
    image: str

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    teacher: Optional[Teacher] = None
    student: Optional[Student] = None
    level: Optional[ScoreLevel] = None

    class Config:
        from_attributes = True


class TeacherListResponse(BaseModel):
    id: int
    created_at: datetime
    name: str
    level: ScoreLevel
    teacher: Teacher
    system_score: float
    school_name: str
    address_line_one: str
    city: str
    province: str
    dob: datetime
    image: Optional[str] = None
    cover_image: Optional[str] = None
    bio: Optional[str] = None
    is_verified: Optional[bool] = None
    role_id: Optional[int] = None
    sex: Optional[SexEnum] = None

    class Config:
        from_attributes = True


class StudentListResponse(BaseModel):
    id: int
    created_at: datetime
    name: str
    level: ScoreLevel
    student: Student
    system_score: float
    school_name: str
    address_line_one: str
    city: str
    province: str
    dob: datetime
    image: Optional[str] = None
    cover_image: Optional[str] = None
    bio: Optional[str] = None
    is_verified: Optional[bool] = None
    role_id: Optional[int] = None
    sex: Optional[SexEnum] = None

    class Config:
        from_attributes = True
