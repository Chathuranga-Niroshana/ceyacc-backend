from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class SexEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class UserBase(BaseModel):
    image: Optional[str] = None
    cover_image: Optional[str] = None
    name: str
    bio: Optional[str] = None
    email: EmailStr
    mobile_no: Optional[str] = None
    dob: Optional[datetime] = None
    system_score: Optional[float] = None
    school_name: Optional[str] = None
    address_line_one: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    sex: Optional[SexEnum] = None
    nic: Optional[str] = None
    is_verified: Optional[bool] = True
    role_id: Optional[int] = 1


# Schema for creating a user (password required)
class UserCreate(UserBase):
    password: str


# Schema for updating a user (all optional)
class UserUpdate(BaseModel):
    image: Optional[str] = None
    cover_image: Optional[str] = None
    name: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    mobile_no: Optional[str] = None
    dob: Optional[datetime] = None
    system_score: Optional[float] = None
    school_name: Optional[str] = None
    address_line_one: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    sex: Optional[SexEnum] = None
    nic: Optional[str] = None
    is_verified: Optional[bool] = None
    role_id: Optional[int] = None


# Schema for response (output), including id and timestamps
class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
