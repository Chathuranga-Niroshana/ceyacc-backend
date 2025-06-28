import logging
from app.models.post_reaction import PostReactions
from sqlalchemy.orm import Session
from app.schemas.post import ReactionCreate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.core.exceptions import (
    DatabaseError,
    ValidationError,
    NotFoundError,
)
import logging
from app.services.format_comment import format_comment

logger = logging.getLogger(__name__)


class CRUDPostReaction:
    # create
    def react_to_a_post(self, db: Session, new_react: ReactionCreate, user_id: int):
        try:

            existing_react = (
                db.query(PostReactions)
                .filter(
                    PostReactions.post_id == new_react.post_id,
                    PostReactions.user_id == user_id,
                )
                .first()
            )
            if (
                existing_react
                and existing_react.reaction_type_id != new_react.reaction_type_id
            ):
                existing_react.reaction_type_id = new_react.reaction_type_id
                db.commit()
                db.refresh(existing_react)
                logger.info("react updated")
                return None
            elif (
                existing_react
                and existing_react.reaction_type_id == new_react.reaction_type_id
            ):
                db.delete(existing_react)
                db.commit()
                logger.info("react deleted")
                return
            else:
                react = PostReactions(
                    reaction_type_id=new_react.reaction_type_id,
                    post_id=new_react.post_id,
                    user_id=user_id,
                )
                db.add(react)
                db.flush()
                db.commit()
                logger.info("Reacted Successfully")
                return react
        except IntegrityError as e:
            db.rollback()
            logger.error(f"error reacting: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"error reacting: {str(e)}")
            raise DatabaseError("Failed to react")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error reacting: {str(e)}")


crud_reactions = CRUDPostReaction()
