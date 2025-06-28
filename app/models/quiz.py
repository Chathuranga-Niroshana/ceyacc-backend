from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255))
    question = Column(String(255))
    description = Column(String(255))
    media_url_one = Column(String(255))
    media_url_two = Column(String(255))
    media_url_three = Column(String(255))
    answer_one = Column(String(255))
    answer_two = Column(String(255))
    answer_three = Column(String(255))
    answer_four = Column(String(255))
    answer_five = Column(String(255))
    correct_answer = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    visibility = Column(Boolean, default=True)

    user = relationship("User", back_populates="post_rating")
