import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.user import UserFullCreate, User as UserSchema, UserUpdate
from app.crud.crud_user import crud_user
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ValidationError, DatabaseError, NotFoundError
from app.db.deps import get_db
from app.services.user_response_builder import (
    build_user_response,
    build_student_list_response,
    build_teacher_list_response,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["Users"])


# register
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserFullCreate, db: Session = Depends(get_db)):
    try:
        user = crud_user.create_user(db=db, user_in=user_in)
        logger.info(f"User registered successfully: {user.email}")

        return build_user_response(user, db)

    except ValidationError as e:
        logger.warning(f"Validation error in user registration: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error in user registration: {str(e)}")
        raise DatabaseError("Unexpected error occurred while creating user")


# get user by id
@router.get("/get/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user = crud_user.get_user_by_id(db, user_id)
        if not user:
            return NotFoundError("User not found")
        return build_user_response(user, db)
    except Exception as e:
        logger.error(f"Unexpected error fetching user by ID: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving user by id")


# get user by email
@router.get("/get")
def get_user_by_email(email: str = Query(...), db: Session = Depends(get_db)):
    try:
        user = crud_user.get_user_by_email(db, email)
        if not user:
            return NotFoundError("User with email not found")
        return build_user_response(user, db)
    except Exception as e:
        logger.error(f"Unexpected error fetching user by Email: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving user")


# get teachers
@router.get("/teachers")
def get_teachers(db: Session = Depends(get_db)):
    try:
        teachers = crud_user.get_teachers(db)
        if not teachers:
            return NotFoundError("Teachers not found")
        formatted_teachers = []
        for teacher in teachers:
            formatted_teacher = build_teacher_list_response(teacher, db)
            formatted_teachers.append(formatted_teacher)

        return formatted_teachers
    except Exception as e:
        logger.error(f"Unexpected error fetching Teachers: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving Teachers")


# get students
@router.get("/students")
def get_students(db: Session = Depends(get_db)):
    try:
        students = crud_user.get_students(db)
        if not students:
            return NotFoundError("Students not found")
        formatted_students = []
        for student in students:
            formatted_students.append(build_student_list_response(student, db))

        return formatted_students
    except Exception as e:
        logger.error(f"Unexpected error fetching Students: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving Students")


# Most engaging users
@router.get("/most_engaging", status_code=status.HTTP_200_OK)
def get_most_engaging_users(db: Session = Depends(get_db)):
    try:
        users = crud_user.get_most_engaging_users(db)
        return [build_user_response(user, db) for user in users]
    except Exception as e:
        logger.error(f"Unexpected error fetching most engaging users: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving most engaging users")


# update user
@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update user profile. Editable fields:
    - name
    - email
    - password
    - bio
    - image
    - cover_image
    - mobile_no
    - dob
    - school_name
    - address_line_one
    - city
    - province
    - sex
    - nic
    - is_verified
    - role_id
    - teacher: { subjects_taught, teaching_experience }
    - student: { grade, is_completed }
    """
    try:
        user = crud_user.update_user(db=db, user_id=user_id, user_update=user_update)
        return build_user_response(user, db)
    except ValidationError as e:
        logger.warning(f"Validation error in user update: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating user: {str(e)}")
        raise DatabaseError("Unexpected error occurred while updating user")
