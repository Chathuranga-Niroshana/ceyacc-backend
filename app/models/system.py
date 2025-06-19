from sqlalchemy import Column, Integer, String
from app.db.base import Base


class UserRoles(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10))


class ScoreLevels(Base):
    __tablename__ = "score_levels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10))
    image = Column(String(255))
    max_limit = Column(Integer)


# user role
# 1 => student
# 2 => teacher
# 3 => admin
