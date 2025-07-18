import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.course import Course, CourseQuestion, CourseAnswer
from app.schemas.course import CourseCreate, CourseResponse
from app.core.exceptions import (
    DatabaseError, ValidationError, NotFoundError, AuthorizationError
)
from datetime import datetime

logger = logging.getLogger(__name__)

class CRUDCourse:
    def create_course(self, db: Session, new_course: CourseCreate):
        try:
            # Map media/resources/thumbnail lists to columns
            media = new_course.media or []
            resources = new_course.resources or []
            thumbnail = new_course.thumbnail or []
            course = Course(
                title=new_course.title,
                description=new_course.description,
                thumbnail_url=thumbnail[0] if thumbnail else None,
                media_url_1=media[0] if len(media) > 0 else None,
                media_url_2=media[1] if len(media) > 1 else None,
                media_url_3=media[2] if len(media) > 2 else None,
                media_url_4=media[3] if len(media) > 3 else None,
                media_url_5=media[4] if len(media) > 4 else None,
                media_url_6=media[5] if len(media) > 5 else None,
                media_url_7=media[6] if len(media) > 6 else None,
                media_url_8=media[7] if len(media) > 7 else None,
                media_url_9=media[8] if len(media) > 8 else None,
                media_url_10=media[9] if len(media) > 9 else None,
                media_url_11=media[10] if len(media) > 10 else None,
                media_url_12=media[11] if len(media) > 11 else None,
                media_url_13=media[12] if len(media) > 12 else None,
                media_url_14=media[13] if len(media) > 13 else None,
                media_url_15=media[14] if len(media) > 14 else None,
                resource_url_1=resources[0] if len(resources) > 0 else None,
                resource_url_2=resources[1] if len(resources) > 1 else None,
                resource_url_3=resources[2] if len(resources) > 2 else None,
                resource_url_4=resources[3] if len(resources) > 3 else None,
                resource_url_5=resources[4] if len(resources) > 4 else None,
                marks_for_pass=new_course.marks_for_pass,
                applicable_grade=new_course.applicable_grade,
                applicable_level=new_course.applicable_level,
            )
            db.add(course)
            db.flush()
            # Add questions and answers
            for q in new_course.questions:
                question = CourseQuestion(
                    course_id=course.id,
                    question=q.question,
                    correct_answer=q.correct_answer,
                    marks=q.marks,
                )
                db.add(question)
                db.flush()
                for ans in q.answers:
                    answer = CourseAnswer(
                        question_id=question.id,
                        answer=ans,
                    )
                    db.add(answer)
            db.commit()
            db.refresh(course)
            logger.info("Course created successfully")
            return course
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error creating course: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating course: {str(e)}")
            raise DatabaseError("Failed to create course")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating course: {str(e)}")
            raise DatabaseError("An unexpected error occurred")

    def get_course_by_id(self, db: Session, course_id: int):
        try:
            course = db.get(Course, course_id)
            if not course:
                raise NotFoundError("Course not found")
            # Build media/resources/thumbnail lists
            media = [getattr(course, f"media_url_{i}") for i in range(1, 16) if getattr(course, f"media_url_{i}")]
            resources = [getattr(course, f"resource_url_{i}") for i in range(1, 6) if getattr(course, f"resource_url_{i}")]
            thumbnail = [course.thumbnail_url] if course.thumbnail_url else []
            # Build questions and answers
            questions = []
            for q in course.questions:
                answers = [a.answer for a in q.answers]
                questions.append({
                    "id": q.id,
                    "question": q.question,
                    "answers": answers,
                    "correctAnswer": q.correct_answer,
                    "marks": q.marks,
                })
            return {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "thumbnail": thumbnail,
                "media": media,
                "resources": resources,
                "marksForPass": course.marks_for_pass,
                "applicableGrade": course.applicable_grade,
                "applicableLevel": course.applicable_level,
                "questions": questions,
                "created_at": course.created_at,
            }
        except SQLAlchemyError as e:
            logger.error(f"Error fetching course by id: {str(e)}")
            raise DatabaseError("Failed to fetch course by id")

    def get_courses(self, db: Session):
        try:
            courses = db.query(Course).all()
            if not courses:
                raise NotFoundError("No courses found")
            response_courses = []
            for course in courses:
                media = [getattr(course, f"media_url_{i}") for i in range(1, 16) if getattr(course, f"media_url_{i}")]
                resources = [getattr(course, f"resource_url_{i}") for i in range(1, 6) if getattr(course, f"resource_url_{i}")]
                thumbnail = [course.thumbnail_url] if course.thumbnail_url else []
                questions = []
                for q in course.questions:
                    answers = [a.answer for a in q.answers]
                    questions.append({
                        "id": q.id,
                        "question": q.question,
                        "answers": answers,
                        "correctAnswer": q.correct_answer,
                        "marks": q.marks,
                    })
                formatted_course = {
                    "id": course.id,
                    "title": course.title,
                    "description": course.description,
                    "thumbnail": thumbnail,
                    "media": media,
                    "resources": resources,
                    "marksForPass": course.marks_for_pass,
                    "applicableGrade": course.applicable_grade,
                    "applicableLevel": course.applicable_level,
                    "questions": questions,
                    "created_at": course.created_at,
                }
                response_courses.append(formatted_course)
            return response_courses
        except SQLAlchemyError as e:
            logger.error(f"Error fetching courses: {str(e)}")
            raise DatabaseError("Failed to fetch courses")

    def update_course(self, db: Session, course_id: int, course_update: CourseCreate):
        try:
            course = db.get(Course, course_id)
            if not course:
                raise NotFoundError("Course not found")
            # Update simple fields
            course.title = course_update.title
            course.description = course_update.description
            thumbnail = course_update.thumbnail or []
            course.thumbnail_url = thumbnail[0] if thumbnail else None
            media = course_update.media or []
            for i in range(1, 16):
                setattr(course, f"media_url_{i}", media[i-1] if len(media) >= i else None)
            resources = course_update.resources or []
            for i in range(1, 6):
                setattr(course, f"resource_url_{i}", resources[i-1] if len(resources) >= i else None)
            course.marks_for_pass = course_update.marks_for_pass
            course.applicable_grade = course_update.applicable_grade
            course.applicable_level = course_update.applicable_level
            # Remove old questions/answers
            for q in course.questions:
                db.query(CourseAnswer).filter(CourseAnswer.question_id == q.id).delete()
            db.query(CourseQuestion).filter(CourseQuestion.course_id == course.id).delete()
            db.flush()
            # Add new questions/answers
            for q in course_update.questions:
                question = CourseQuestion(
                    course_id=course.id,
                    question=q.question,
                    correct_answer=q.correct_answer,
                    marks=q.marks,
                )
                db.add(question)
                db.flush()
                for ans in q.answers:
                    answer = CourseAnswer(
                        question_id=question.id,
                        answer=ans,
                    )
                    db.add(answer)
            db.commit()
            db.refresh(course)
            logger.info("Course updated successfully")
            return course
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error updating course: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error updating course: {str(e)}")
            raise DatabaseError("Failed to update course")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error updating course: {str(e)}")
            raise DatabaseError("An unexpected error occurred")

    def delete_course(self, db: Session, course_id: int):
        try:
            course = db.get(Course, course_id)
            if not course:
                raise NotFoundError("Course not found")
            db.delete(course)
            db.commit()
            logger.info("Course deleted successfully")
            return True
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error deleting course: {str(e)}")
            raise DatabaseError("Failed to delete course")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error deleting course: {str(e)}")
            raise DatabaseError("An unexpected error occurred")

crud_course = CRUDCourse()
