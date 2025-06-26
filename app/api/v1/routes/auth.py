import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import User as UserSchema
from app.db.deps import get_db
from app.services.user_response_builder import build_user_response
from app.crud.crud_auth import login_user as login
from app.core.exceptions import NotFoundError, AuthenticationError, DatabaseError
from app.schemas.auth import LoginRequest
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    try:
        data = login(db, credentials)
        user = data["user"]
        token = data["token"]

        response = build_user_response(user, db)
        return {"success": True, "user": response, "token": token}

    except (NotFoundError, AuthenticationError) as e:
        return JSONResponse(
            status_code=401, content={"success": False, "message": str(e)}
        )
    except DatabaseError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": str(e)},
        )
    except Exception as e:
        logger.error(f"Unexpected login error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Unexpected error occurred"},
        )
