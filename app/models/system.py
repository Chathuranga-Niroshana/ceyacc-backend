from sqlalchemy import Column, Integer, String, Enum
from app.db.base import Base
import enum
from sqlalchemy.orm import relationship


class UserRoles(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10))

    users = relationship("User", back_populates="user_role")


class ScoreLevels(Base):
    __tablename__ = "score_levels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    image = Column(String(255))
    max_limit = Column(Integer)


class SexEnum(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class TeachingExperienceEnum(enum.Enum):
    BEGINNER = "0-1 Years"
    INTERMEDIATE = "1-4 Years"
    EXPERIENCED = "4-10 Years"
    MASTER = "10+ years"
