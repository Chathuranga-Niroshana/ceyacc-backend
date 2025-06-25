from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
    Enum,
    Boolean,
    JSON,
)
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
from app.models.system import SexEnum, TeachingExperienceEnum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image = Column(String(255))
    cover_image = Column(String(255))
    name = Column(String(100), nullable=False)
    bio = Column(String(255))
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    mobile_no = Column(String(13))
    dob = Column(DateTime)
    system_score = Column(Float, default=10.00)
    school_name = Column(String(255))
    address_line_one = Column(String(255))
    city = Column(String(100))
    province = Column(String(100))
    sex = Column(Enum(SexEnum), nullable=True)
    nic = Column(String(12), nullable=True, unique=True)
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    role_id = Column(Integer, ForeignKey("user_roles.id"), default=1)

    user_role = relationship("UserRoles", back_populates="users")
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    student = relationship("Student", back_populates="user")


class Teacher(Base):
    __tablename__ = "teacher_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    subjects_taught = Column(JSON)
    teaching_experience = Column(Enum(TeachingExperienceEnum), nullable=True)

    user = relationship("User", back_populates="teacher")


class Student(Base):
    __tablename__ = "student_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    grade = Column(Integer)
    is_completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="student")
