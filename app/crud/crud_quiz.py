import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.quiz import Quiz, QuizInteraction
from app.models.user import User
from app.schemas.quiz import (
    QuizCreate, QuizResponse, QuizInteractionCreate, QuizInteractionResponse, UserPreview
)
from app.core.exceptions import (
    DatabaseError, ValidationError, NotFoundError, AuthorizationError
)
from datetime import datetime

logger = logging.getLogger(__name__)

class CRUDQuiz:
    # Create quiz
    def create_quiz(self, db: Session, new_quiz: QuizCreate, user_id: int):
        try:
            quiz = Quiz(
                title=new_quiz.title,
                question=new_quiz.question,
                description=new_quiz.description,
                media_url_one=new_quiz.media_url_one,
                media_url_two=new_quiz.media_url_two,
                media_url_three=new_quiz.media_url_three,
                answer_one=new_quiz.answer_one,
                answer_two=new_quiz.answer_two,
                answer_three=new_quiz.answer_three,
                answer_four=new_quiz.answer_four,
                answer_five=new_quiz.answer_five,
                correct_answer=new_quiz.correct_answer,
                user_id=user_id,
                visibility=new_quiz.visibility if new_quiz.visibility is not None else True,
            )
            db.add(quiz)
            db.flush()
            db.commit()
            db.refresh(quiz)
            logger.info("Quiz created successfully")
            return quiz
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error creating quiz: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating quiz: {str(e)}")
            raise DatabaseError("Failed to create quiz")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating quiz: {str(e)}")
            raise DatabaseError("An unexpected error occurred")

    # Get quiz by id
    def get_quiz_by_id(self, db: Session, quiz_id: int, user_id: int):
        try:
            quiz = db.get(Quiz, quiz_id)
            if not quiz:
                raise NotFoundError("Quiz not found")
            if not quiz.visibility and quiz.user_id != user_id:
                raise AuthorizationError("Not authorized to view this quiz")
            user = db.get(User, quiz.user_id)
            user_preview = UserPreview(id=user.id, name=user.name, image=user.image)
            return QuizResponse(
                id=quiz.id,
                title=quiz.title,
                question=quiz.question,
                description=quiz.description,
                media_url_one=quiz.media_url_one,
                media_url_two=quiz.media_url_two,
                media_url_three=quiz.media_url_three,
                answer_one=quiz.answer_one,
                answer_two=quiz.answer_two,
                answer_three=quiz.answer_three,
                answer_four=quiz.answer_four,
                answer_five=quiz.answer_five,
                correct_answer=quiz.correct_answer,
                visibility=quiz.visibility,
                user=user_preview,
                created_at=quiz.created_at,
            )
        except SQLAlchemyError as e:
            logger.error(f"Error fetching quiz by id: {str(e)}")
            raise DatabaseError("Failed to fetch quiz by id")

    # Get all quizzes
    def get_quizzes(self, db: Session, user_id: int):
        try:
            quizzes = db.query(Quiz).all()
            if not quizzes:
                raise NotFoundError("No quizzes found")
            response_quizzes = []
            for quiz in quizzes:
                if not quiz.visibility and quiz.user_id != user_id:
                    continue
                user = db.get(User, quiz.user_id)
                user_preview = UserPreview(id=user.id, name=user.name, image=user.image)
                formatted_quiz = QuizResponse(
                    id=quiz.id,
                    title=quiz.title,
                    question=quiz.question,
                    description=quiz.description,
                    media_url_one=quiz.media_url_one,
                    media_url_two=quiz.media_url_two,
                    media_url_three=quiz.media_url_three,
                    answer_one=quiz.answer_one,
                    answer_two=quiz.answer_two,
                    answer_three=quiz.answer_three,
                    answer_four=quiz.answer_four,
                    answer_five=quiz.answer_five,
                    correct_answer=quiz.correct_answer,
                    visibility=quiz.visibility,
                    user=user_preview,
                    created_at=quiz.created_at,
                )
                response_quizzes.append(formatted_quiz)
            return response_quizzes
        except SQLAlchemyError as e:
            logger.error(f"Error fetching quizzes: {str(e)}")
            raise DatabaseError("Failed to fetch quizzes")

    # Update quiz
    def update_quiz(self, db: Session, quiz_id: int, quiz_update: QuizCreate, user_id: int):
        try:
            quiz = db.get(Quiz, quiz_id)
            if not quiz:
                raise NotFoundError("Quiz not found")
            if quiz.user_id != user_id:
                raise AuthorizationError("Not authorized to update this quiz")
            for field, value in quiz_update.dict(exclude_unset=True).items():
                setattr(quiz, field, value)
            db.commit()
            db.refresh(quiz)
            logger.info("Quiz updated successfully")
            return quiz
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error updating quiz: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error updating quiz: {str(e)}")
            raise DatabaseError("Failed to update quiz")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error updating quiz: {str(e)}")
            raise DatabaseError("An unexpected error occurred")

    # Delete quiz
    def delete_quiz(self, db: Session, quiz_id: int, user_id: int):
        try:
            quiz = db.get(Quiz, quiz_id)
            if not quiz:
                raise NotFoundError("Quiz not found")
            if quiz.user_id != user_id:
                raise AuthorizationError("Not authorized to delete this quiz")
            db.delete(quiz)
            db.commit()
            logger.info("Quiz deleted successfully")
            return True
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error deleting quiz: {str(e)}")
            raise DatabaseError("Failed to delete quiz")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error deleting quiz: {str(e)}")
            raise DatabaseError("An unexpected error occurred")

    # Create quiz interaction (answer)
    def create_quiz_interaction(self, db: Session, quiz_id: int, user_id: int, interaction: QuizInteractionCreate):
        try:
            quiz = db.get(Quiz, quiz_id)
            if not quiz:
                raise NotFoundError("Quiz not found")
            quiz_interaction = QuizInteraction(
                user_id=user_id,
                quiz_id=quiz_id,
                answer_id=interaction.answer_id,
            )
            db.add(quiz_interaction)
            db.flush()
            db.commit()
            db.refresh(quiz_interaction)
            logger.info("Quiz interaction created successfully")
            user = db.get(User, user_id)
            user_preview = UserPreview(id=user.id, name=user.name, image=user.image)
            return QuizInteractionResponse(
                id=quiz_interaction.id,
                user=user_preview,
                quiz_id=quiz_id,
                answer_id=quiz_interaction.answer_id,
                created_at=quiz_interaction.created_at,
            )
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error creating quiz interaction: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating quiz interaction: {str(e)}")
            raise DatabaseError("Failed to create quiz interaction")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating quiz interaction: {str(e)}")
            raise DatabaseError("An unexpected error occurred")

    # Get all interactions for a quiz
    def get_quiz_interactions(self, db: Session, quiz_id: int):
        try:
            interactions = db.query(QuizInteraction).filter(QuizInteraction.quiz_id == quiz_id).all()
            if not interactions:
                raise NotFoundError("No interactions found for this quiz")
            response_interactions = []
            for interaction in interactions:
                user = db.get(User, interaction.user_id)
                user_preview = UserPreview(id=user.id, name=user.name, image=user.image)
                formatted_interaction = QuizInteractionResponse(
                    id=interaction.id,
                    user=user_preview,
                    quiz_id=interaction.quiz_id,
                    answer_id=interaction.answer_id,
                    created_at=interaction.created_at,
                )
                response_interactions.append(formatted_interaction)
            return response_interactions
        except SQLAlchemyError as e:
            logger.error(f"Error fetching quiz interactions: {str(e)}")
            raise DatabaseError("Failed to fetch quiz interactions")

crud_quiz = CRUDQuiz()
