import logging
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.schemas.exam_paper import ExamPaperCreate, ExamPaperUpdate, ExamPaperResponse
from app.crud.crud_exam_paper import crud_exam_paper
from app.core.exceptions import (
    ValidationError,
    DatabaseError,
    NotFoundError,
    AuthorizationError,
)
from app.db.deps import get_db
from typing import List

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/exam_papers", tags=["Exam Papers"])

# Create exam paper
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_exam_paper(new_exam_paper: ExamPaperCreate, db: Session = Depends(get_db)):
    try:
        crud_exam_paper.create_exam_paper(db=db, new_exam_paper=new_exam_paper)
        logger.info("Exam paper created")
        return {"message": "Exam paper created successfully"}
    except ValidationError as e:
        logger.warning(f"Validation error in exam paper create: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error in exam paper create: {str(e)}")
        raise DatabaseError("Unexpected error occurred while creating exam paper")

# Get exam paper by id
@router.get("/get/{exam_paper_id}", response_model=ExamPaperResponse, status_code=status.HTTP_200_OK)
async def get_exam_paper_by_id(exam_paper_id: int, db: Session = Depends(get_db)):
    try:
        exam_paper = crud_exam_paper.get_exam_paper_by_id(db=db, exam_paper_id=exam_paper_id)
        if not exam_paper:
            raise NotFoundError("Exam paper not found")
        return exam_paper
    except NotFoundError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching exam paper by ID: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving exam paper")

# Get all exam papers
@router.get("/get_all", response_model=List[ExamPaperResponse], status_code=status.HTTP_200_OK)
async def get_exam_papers(db: Session = Depends(get_db)):
    try:
        exam_papers = crud_exam_paper.get_exam_papers(db=db)
        if not exam_papers:
            raise NotFoundError("Exam papers not available")
        return exam_papers
    except NotFoundError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching exam papers: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving exam papers")

# Update exam paper
@router.put("/update/{exam_paper_id}", status_code=status.HTTP_200_OK)
async def update_exam_paper(exam_paper_id: int, exam_paper_update: ExamPaperUpdate, db: Session = Depends(get_db)):
    try:
        crud_exam_paper.update_exam_paper(db=db, exam_paper_id=exam_paper_id, exam_paper_update=exam_paper_update)
        logger.info("Exam paper updated")
        return {"message": "Exam paper updated successfully"}
    except ValidationError as e:
        logger.warning(f"Validation error in exam paper update: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating exam paper: {str(e)}")
        raise DatabaseError("Unexpected error occurred while updating exam paper")

# Delete exam paper
@router.delete("/delete/{exam_paper_id}", status_code=status.HTTP_200_OK)
async def delete_exam_paper(exam_paper_id: int, db: Session = Depends(get_db)):
    try:
        crud_exam_paper.delete_exam_paper(db=db, exam_paper_id=exam_paper_id)
        logger.info("Exam paper deleted")
        return {"message": "Exam paper deleted successfully"}
    except NotFoundError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error deleting exam paper: {str(e)}")
        raise DatabaseError("Unexpected error occurred while deleting exam paper")
