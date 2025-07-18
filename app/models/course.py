from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    thumbnail_url = Column(String(255))
    # Up to 15 media URLs
    media_url_1 = Column(String(255))
    media_url_2 = Column(String(255))
    media_url_3 = Column(String(255))
    media_url_4 = Column(String(255))
    media_url_5 = Column(String(255))
    media_url_6 = Column(String(255))
    media_url_7 = Column(String(255))
    media_url_8 = Column(String(255))
    media_url_9 = Column(String(255))
    media_url_10 = Column(String(255))
    media_url_11 = Column(String(255))
    media_url_12 = Column(String(255))
    media_url_13 = Column(String(255))
    media_url_14 = Column(String(255))
    media_url_15 = Column(String(255))
    # Up to 5 resource URLs
    resource_url_1 = Column(String(255))
    resource_url_2 = Column(String(255))
    resource_url_3 = Column(String(255))
    resource_url_4 = Column(String(255))
    resource_url_5 = Column(String(255))
    marks_for_pass = Column(Integer)
    applicable_grade = Column(String(10))
    applicable_level = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("CourseQuestion", back_populates="course", cascade="all, delete-orphan")

class CourseQuestion(Base):
    __tablename__ = "course_questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    question = Column(Text, nullable=False)
    correct_answer = Column(Integer, nullable=False)
    marks = Column(Integer, nullable=False)

    course = relationship("Course", back_populates="questions")
    answers = relationship("CourseAnswer", back_populates="question", cascade="all, delete-orphan")

class CourseAnswer(Base):
    __tablename__ = "course_answers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("course_questions.id"), nullable=False)
    answer = Column(Text, nullable=False)

    question = relationship("CourseQuestion", back_populates="answers")
