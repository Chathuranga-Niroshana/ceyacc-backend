import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.user import UserFullCreate, User as UserSchema
from app.crud.crud_user import crud_user
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ValidationError, DatabaseError, NotFoundError
from app.db.deps import get_db
from app.services.user_response_builder import build_user_response

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
        raise DatabaseError("Unexpected error occurred while retrieving user")


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
