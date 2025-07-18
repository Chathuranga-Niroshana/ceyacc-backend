import logging
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.schemas.quiz import QuizCreate, QuizResponse, QuizInteractionCreate, QuizInteractionResponse
from app.crud.crud_quiz import crud_quiz
from app.core.exceptions import (
    ValidationError,
    DatabaseError,
    NotFoundError,
    AuthorizationError,
)
from app.db.deps import get_db
from typing import List

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

# Create quiz
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_quiz(request: Request, new_quiz: QuizCreate, db: Session = Depends(get_db)):
    try:
        user = request.state.user
        crud_quiz.create_quiz(db=db, new_quiz=new_quiz, user_id=user.id)
        logger.info("Quiz created")
        return {"message": "Quiz created successfully"}
    except ValidationError as e:
        logger.warning(f"Validation error in quiz create: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error in quiz create: {str(e)}")
        raise DatabaseError("Unexpected error occurred while creating quiz")

# Get quiz by id
@router.get("/get/{quiz_id}", response_model=QuizResponse, status_code=status.HTTP_200_OK)
async def get_quiz_by_id(request: Request, quiz_id: int, db: Session = Depends(get_db)):
    try:
        user = request.state.user
        quiz = crud_quiz.get_quiz_by_id(db=db, quiz_id=quiz_id, user_id=user.id)
        if not quiz:
            raise NotFoundError("Quiz not found")
        return quiz
    except NotFoundError as e:
        logger.warning(str(e))
        raise e
    except AuthorizationError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching quiz by ID: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving quiz")

# Get all quizzes
@router.get("/get_all", response_model=List[QuizResponse], status_code=status.HTTP_200_OK)
async def get_quizzes(request: Request, db: Session = Depends(get_db)):
    try:
        user = request.state.user
        quizzes = crud_quiz.get_quizzes(db=db, user_id=user.id)
        if not quizzes:
            raise NotFoundError("Quizzes not available")
        return quizzes
    except NotFoundError as e:
        logger.warning(str(e))
        raise e
    except AuthorizationError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching quizzes: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving quizzes")

# Update quiz
@router.put("/update/{quiz_id}", status_code=status.HTTP_200_OK)
async def update_quiz(request: Request, quiz_id: int, quiz_update: QuizCreate, db: Session = Depends(get_db)):
    try:
        user = request.state.user
        crud_quiz.update_quiz(db=db, quiz_id=quiz_id, quiz_update=quiz_update, user_id=user.id)
        logger.info("Quiz updated")
        return {"message": "Quiz updated successfully"}
    except ValidationError as e:
        logger.warning(f"Validation error in quiz update: {str(e)}")
        raise ValidationError(str(e))
    except AuthorizationError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error updating quiz: {str(e)}")
        raise DatabaseError("Unexpected error occurred while updating quiz")

# Delete quiz
@router.delete("/delete/{quiz_id}", status_code=status.HTTP_200_OK)
async def delete_quiz(request: Request, quiz_id: int, db: Session = Depends(get_db)):
    try:
        user = request.state.user
        crud_quiz.delete_quiz(db=db, quiz_id=quiz_id, user_id=user.id)
        logger.info("Quiz deleted")
        return {"message": "Quiz deleted successfully"}
    except NotFoundError as e:
        logger.warning(str(e))
        raise e
    except AuthorizationError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error deleting quiz: {str(e)}")
        raise DatabaseError("Unexpected error occurred while deleting quiz")

# Create quiz interaction (answer)
@router.post("/interact/{quiz_id}", response_model=QuizInteractionResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz_interaction(request: Request, quiz_id: int, interaction: QuizInteractionCreate, db: Session = Depends(get_db)):
    try:
        user = request.state.user
        response = crud_quiz.create_quiz_interaction(db=db, quiz_id=quiz_id, user_id=user.id, interaction=interaction)
        logger.info("Quiz interaction created")
        return response
    except ValidationError as e:
        logger.warning(f"Validation error in quiz interaction: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error in quiz interaction: {str(e)}")
        raise DatabaseError("Unexpected error occurred while creating quiz interaction")

# Get all interactions for a quiz
@router.get("/interactions/{quiz_id}", response_model=List[QuizInteractionResponse], status_code=status.HTTP_200_OK)
async def get_quiz_interactions(request: Request, quiz_id: int, db: Session = Depends(get_db)):
    try:
        interactions = crud_quiz.get_quiz_interactions(db=db, quiz_id=quiz_id)
        if not interactions:
            raise NotFoundError("No interactions found for this quiz")
        return interactions
    except NotFoundError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching quiz interactions: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving quiz interactions")
