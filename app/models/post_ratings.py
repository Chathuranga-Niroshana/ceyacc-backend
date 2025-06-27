from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class PostRatings(Base):
    __tablename__ = "post_ratings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String(255), default="post")
    ratings = Column(Float, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="post_rating")
    user = relationship("User", back_populates="post_rating")
