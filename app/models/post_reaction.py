from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class PostReactions(Base):
    __tablename__ = "post_reactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reaction_type_id = Column(Integer, ForeignKey("reaction_types.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    reaction_type = relationship("ReactionTypes", back_populates="post_reaction")
    post = relationship("Post", back_populates="post_reaction")
    user = relationship("User", back_populates="post_reaction")
