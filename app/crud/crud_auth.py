from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.utils.jwt import create_access_token
from app.utils.security import verify_password
from app.core.exceptions import (
    DatabaseError,
    NotFoundError,
    AuthenticationError,
)
import logging

logger = logging.getLogger(__name__)


def login_user(db: Session, credentials: LoginRequest):
    try:
        clean_email = credentials.email.lower().strip()
        user = db.query(User).filter(User.email == clean_email).first()

        if not user:
            raise NotFoundError("Invalid Email")

        if not verify_password(credentials.password, user.password):
            raise AuthenticationError("Invalid Password")

        token_data = {"user_id": user.id, "role_id": user.role_id}
        access_token = create_access_token(token_data)
        return {"user": user, "token": access_token}
    except (NotFoundError, AuthenticationError):
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise DatabaseError("Login Failed")
