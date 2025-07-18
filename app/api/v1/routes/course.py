import logging
from fastapi import APIRouter, Depends, status, Request 
from sqlalchemy.orm import Session
from app.schemas.course import CourseCreate, CourseResponse
from app.crud.crud_course import crud_course
from app.core.exceptions import (
    ValidationError,
    DatabaseError,
    NotFoundError,
    AuthorizationError,
)
from app.db.deps import get_db
from typing import List
from app.services.interaction_score_update import update_user_score
from app.constants.score_update_values import SCORE_UPDATE_VALUES

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/courses", tags=["Courses"])

# Create course
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_course(request: Request, new_course: CourseCreate, db: Session = Depends(get_db)):
    try:
        user = request.state.user
        crud_course.create_course(db=db, new_course=new_course)
        logger.info("Course created")
        new_score = update_user_score(
            db=db, value=SCORE_UPDATE_VALUES["CREATE_COURSE"], user_id=user.id
        )
        logger.info(f"User {user.id} score after course: {new_score}")
        return {"message": "Course created successfully"}
    except ValidationError as e:
        logger.warning(f"Validation error in course create: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error in course create: {str(e)}")
        raise DatabaseError("Unexpected error occurred while creating course")

# Get course by id
@router.get("/get/{course_id}", response_model=CourseResponse, status_code=status.HTTP_200_OK)
async def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    try:
        course = crud_course.get_course_by_id(db=db, course_id=course_id)
        if not course:
            raise NotFoundError("Course not found")
        return course
    except NotFoundError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching course by ID: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving course")

# Get all courses
@router.get("/get_all", response_model=List[CourseResponse], status_code=status.HTTP_200_OK)
async def get_courses(db: Session = Depends(get_db)):
    try:
        courses = crud_course.get_courses(db=db)
        if not courses:
            raise NotFoundError("Courses not available")
        return courses
    except NotFoundError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching courses: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving courses")

# Update course
@router.put("/update/{course_id}", status_code=status.HTTP_200_OK)
async def update_course(course_id: int, course_update: CourseCreate, db: Session = Depends(get_db)):
    try:
        crud_course.update_course(db=db, course_id=course_id, course_update=course_update)
        logger.info("Course updated")
        return {"message": "Course updated successfully"}
    except ValidationError as e:
        logger.warning(f"Validation error in course update: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating course: {str(e)}")
        raise DatabaseError("Unexpected error occurred while updating course")

# Delete course
@router.delete("/delete/{course_id}", status_code=status.HTTP_200_OK)
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        crud_course.delete_course(db=db, course_id=course_id)
        logger.info("Course deleted")
        return {"message": "Course deleted successfully"}
    except NotFoundError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error deleting course: {str(e)}")
        raise DatabaseError("Unexpected error occurred while deleting course")
