from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255))
    date_time = Column(DateTime)
    location = Column(String(255))
    description = Column(String(255))
    media_url_one = Column(String(255))
    media_url_two = Column(String(255))
    media_url_three = Column(String(255))
    media_url_four = Column(String(255))
    media_url_five = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="event")
    event_interests = relationship("EventInterests", back_populates="event")


class EventInterests(Base):
    __tablename__ = "event_interests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    interest_type = Column(String(255), default="INTERESTED")
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="event_interests")
    event = relationship("Event", back_populates="event_interests")
