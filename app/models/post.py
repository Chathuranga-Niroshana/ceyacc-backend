from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
    Boolean,
    JSON,
)
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    media_link = Column(String(255))
    media_type = Column(String(20))
    title = Column(String(255))
    description = Column(String(255))
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="post")
    comment = relationship("Comments", back_populates="post")
    post_reaction = relationship("PostReactions", back_populates="post")
    post_rating = relationship("PostRatings", back_populates="post")
