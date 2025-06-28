import logging
from fastapi import APIRouter, status, Request, Depends
from sqlalchemy.orm import Session
from app.schemas.post import ReactionCreate
from app.crud.crud_post_reactions import crud_reactions
from app.core.exceptions import ValidationError, DatabaseError
from app.db.deps import get_db
from app.constants.score_update_values import SCORE_UPDATE_VALUES
from app.services.interaction_score_update import update_user_score
from typing import List

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/reaction", tags=["Reaction"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def react_to_post(
    request: Request, new_react: ReactionCreate, db: Session = Depends(get_db)
):
    try:
        user = request.state.user
        react = crud_reactions.react_to_a_post(
            db=db, new_react=new_react, user_id=user.id
        )
        update_user_score(
            db=db, value=SCORE_UPDATE_VALUES["REACT_POST"], user_id=user.id
        )
        return {"message": "Success", "react": react}
    except ValidationError as e:
        logger.warning(f"Validation error in create: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error in create: {str(e)}")
        raise DatabaseError("Unexpected error occurred while creating")
