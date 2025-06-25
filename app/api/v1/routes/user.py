import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserFullCreate, User as UserSchema
from app.db.session import SessionLocal
from app.crud.crud_user import create_user
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user with role-specific data",
)
async def register_user(user_in: UserFullCreate, db: Session = Depends(SessionLocal)):
    try:
        return create_user(db=db, user_in=user_in)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email or NIC already exists",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
