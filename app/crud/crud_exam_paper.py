import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.exam_paper import ExamPaper
from app.schemas.exam_paper import ExamPaperCreate, ExamPaperUpdate, ExamPaperResponse
from app.core.exceptions import (
    DatabaseError, ValidationError, NotFoundError, AuthorizationError
)
from datetime import datetime

logger = logging.getLogger(__name__)

class CRUDExamPaper:
    # Create exam paper
    def create_exam_paper(self, db: Session, new_exam_paper: ExamPaperCreate):
        try:
            # Map media list to individual media_url fields
            media = new_exam_paper.media or []
            media_url_one = media[0] if len(media) > 0 else None
            media_url_two = media[1] if len(media) > 1 else None
            media_url_three = media[2] if len(media) > 2 else None
            exam_paper = ExamPaper(
                subject=new_exam_paper.subject,
                grade=new_exam_paper.grade,
                school=new_exam_paper.school,
                semester=new_exam_paper.semester,
                year=new_exam_paper.year,
                exam_type=new_exam_paper.exam_type,
                description=new_exam_paper.description,
                media_url_one=media_url_one,
                media_url_two=media_url_two,
                media_url_three=media_url_three,
            )
            db.add(exam_paper)
            db.flush()
            db.commit()
            db.refresh(exam_paper)
            logger.info("Exam paper created successfully")
            return exam_paper
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error creating exam paper: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating exam paper: {str(e)}")
            raise DatabaseError("Failed to create exam paper")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating exam paper: {str(e)}")
            raise DatabaseError("An unexpected error occurred")

    # Get exam paper by id
    def get_exam_paper_by_id(self, db: Session, exam_paper_id: int):
        try:
            exam_paper = db.get(ExamPaper, exam_paper_id)
            if not exam_paper:
                raise NotFoundError("Exam paper not found")
            # Build media list
            media = [url for url in [exam_paper.media_url_one, exam_paper.media_url_two, exam_paper.media_url_three] if url]
            return {
                "id": exam_paper.id,
                "subject": exam_paper.subject,
                "grade": exam_paper.grade,
                "school": exam_paper.school,
                "semester": exam_paper.semester,
                "year": exam_paper.year,
                "examType": exam_paper.exam_type,
                "description": exam_paper.description,
                "media": media if media else None,
                "created_at": exam_paper.created_at,
            }
        except SQLAlchemyError as e:
            logger.error(f"Error fetching exam paper by id: {str(e)}")
            raise DatabaseError("Failed to fetch exam paper by id")

    # Get all exam papers
    def get_exam_papers(self, db: Session):
        try:
            exam_papers = db.query(ExamPaper).all()
            if not exam_papers:
                raise NotFoundError("No exam papers found")
            response_exam_papers = []
            for exam_paper in exam_papers:
                media = [url for url in [exam_paper.media_url_one, exam_paper.media_url_two, exam_paper.media_url_three] if url]
                formatted_exam_paper = {
                    "id": exam_paper.id,
                    "subject": exam_paper.subject,
                    "grade": exam_paper.grade,
                    "school": exam_paper.school,
                    "semester": exam_paper.semester,
                    "year": exam_paper.year,
                    "examType": exam_paper.exam_type,
                    "description": exam_paper.description,
                    "media": media if media else None,
                    "created_at": exam_paper.created_at,
                }
                response_exam_papers.append(formatted_exam_paper)
            return response_exam_papers
        except SQLAlchemyError as e:
            logger.error(f"Error fetching exam papers: {str(e)}")
            raise DatabaseError("Failed to fetch exam papers")

    # Update exam paper
    def update_exam_paper(self, db: Session, exam_paper_id: int, exam_paper_update: ExamPaperUpdate):
        try:
            exam_paper = db.get(ExamPaper, exam_paper_id)
            if not exam_paper:
                raise NotFoundError("Exam paper not found")
            for field, value in exam_paper_update.dict(exclude_unset=True).items():
                setattr(exam_paper, field, value)
            db.commit()
            db.refresh(exam_paper)
            logger.info("Exam paper updated successfully")
            return exam_paper
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error updating exam paper: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error updating exam paper: {str(e)}")
            raise DatabaseError("Failed to update exam paper")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error updating exam paper: {str(e)}")
            raise DatabaseError("An unexpected error occurred")

    # Delete exam paper
    def delete_exam_paper(self, db: Session, exam_paper_id: int):
        try:
            exam_paper = db.get(ExamPaper, exam_paper_id)
            if not exam_paper:
                raise NotFoundError("Exam paper not found")
            db.delete(exam_paper)
            db.commit()
            logger.info("Exam paper deleted successfully")
            return True
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error deleting exam paper: {str(e)}")
            raise DatabaseError("Failed to delete exam paper")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error deleting exam paper: {str(e)}")
            raise DatabaseError("An unexpected error occurred")

crud_exam_paper = CRUDExamPaper()
