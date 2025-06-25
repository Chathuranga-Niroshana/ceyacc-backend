import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserFullCreate, User as UserSchema
from app.crud.crud_user import crud_user
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ValidationError, DatabaseError
from app.db.deps import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user with role-specific data",
)
async def register_user(user_in: UserFullCreate, db: Session = Depends(get_db)):
    try:
        user = crud_user.create_user(db=db, user_in=user_in)
        logger.info(f"User registered successfully: {user.email}")

        return {
            "data": user,
            "message": "User registered successfully",
            "success": True,
        }

    except ValidationError as e:
        logger.warning(f"Validation error in user registration: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in user registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user",
        )
    except Exception as e:
        logger.error(f"Unexpected error in user registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
