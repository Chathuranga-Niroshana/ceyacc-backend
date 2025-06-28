import logging
from fastapi import APIRouter, status, Request, Depends
from sqlalchemy.orm import Session
from app.schemas.post import CommentCreate, CommentResponse
from app.crud.crud_comment import crud_comment
from app.core.exceptions import (
    ValidationError,
    DatabaseError,
    NotFoundError,
    AuthorizationError,
)
from app.db.deps import get_db
from app.constants.score_update_values import SCORE_UPDATE_VALUES
from app.services.interaction_score_update import update_user_score
from typing import List


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/comments", tags=["Comments"])


# create
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_comment(
    request: Request, new_comment: CommentCreate, db: Session = Depends(get_db)
):
    try:
        user = request.state.user
        crud_comment.create_comment(db=db, new_comment=new_comment, user_id=user.id)
        update_user_score(
            db=db, value=SCORE_UPDATE_VALUES["COMMENT_POST"], user_id=user.id
        )
        return {"message": "Commented"}
    except ValidationError as e:
        logger.warning(f"Validation error in create: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error in create: {str(e)}")
        raise DatabaseError("Unexpected error occurred while creating")


# get comments by post id
@router.get(
    "/get/{post_id}",
    response_model=List[CommentResponse],
    status_code=status.HTTP_200_OK,
)
async def get_comments_by_post_id(
    request: Request, post_id: int, db: Session = Depends(get_db)
):
    try:
        comments = crud_comment.get_comments_by_post_id(db=db, post_id=post_id)
        if not comments:
            raise NotFoundError("Comments Not Available")
        return comments
    except NotFoundError as e:
        logger.warning(str(e))
        raise e
    except AuthorizationError as e:
        logger.warning(str(e))
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching comments: {str(e)}")
        raise DatabaseError("Unexpected error occurred while retrieving comments")
