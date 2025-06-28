import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from app.schemas.post import PostCreate, PostResponse
from app.crud.crud_post import crud_post
from app.core.exceptions import (
    ValidationError,
    DatabaseError,
    NotFoundError,
    AuthorizationError,
)
from app.db.deps import get_db
from fastapi.responses import JSONResponse
from app.constants.score_update_values import SCORE_UPDATE_VALUES
from app.services.interaction_score_update import update_user_score

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/posts", tags=["Posts"])


# cerate
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(
    request: Request, new_post: PostCreate, db: Session = Depends(get_db)
):
    try:
        user = request.state.user
        crud_post.create_post(db=db, new_post=new_post, user_id=user.id)
        logger.info("Post created")
        new_score = update_user_score(
            db=db, value=SCORE_UPDATE_VALUES["CREATE_POST"], user_id=user.id
        )
        logger.info(f"User {user.id} score after post: {new_score}")
        return {"message": "Post created successfully"}
    except ValidationError as e:
        logger.warning(f"Validation error in post create: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error in post create: {str(e)}")
        raise DatabaseError("Unexpected error occurred while creating post")


# get by id
@router.get(
    "/get/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK
)
async def get_post_by_id(request: Request, post_id: int, db: Session = Depends(get_db)):
    try:
        user = request.state.user
        post = crud_post.get_post_by_id(db=db, post_id=post_id, user_id=user.id)
        if not post:
            raise NotFoundError("Post not found")
        return post
    except NotFoundError as e:
        logger.warning(str(e))
        raise e
    except AuthorizationError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching post by ID: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving post")
