from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


# {
#   "subject": "Engineering Technology",
#   "grade": "12",
#   "school": "Acc cc",
#   "semester": "First Term",
#   "year": "2025-07-10",
#   "description": "adbwjb dwbajb",
#   "media": [],
#   "question": "",
#   "examType": "al",
#   "subjectStream": "technology"
# }
# {
#   "subject": "Buddhism",
#   "grade": "7",
#   "school": "cas csaz",
#   "semester": "First Term",
#   "year": "2025-08-01",
#   "description": "cbjasbcjkb dbsjbja",
#   "media": [
#     "https://your-backend.com/uploads/soft-vision-logo.png",
#     "https://your-backend.com/uploads/soft-vision-logo.png",
#     "https://your-backend.com/uploads/d31d6hy-f1a8638f-6ba4-4e3d-b8b7-91cd9cfc8a10.jpg"
#   ],
#   "examType": "ol"
# }

class ExamPaper(Base):
    __tablename__ = "exam_papers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subject = Column(String(255))
    grade = Column(Integer)
    school = Column(String(255))
    semester = Column(String(255))
    year = Column(String(255))
    exam_type = Column(String(255))
    description = Column(String(255))
    media_url_one = Column(String(255))
    media_url_two = Column(String(255))
    media_url_three = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
