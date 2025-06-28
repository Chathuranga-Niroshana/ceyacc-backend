from sqlalchemy.orm import Session
from app.models.comment import Comments
from app.schemas.post import CommentResponse, CommentCreate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.core.exceptions import (
    DatabaseError,
    ValidationError,
    NotFoundError,
)
import logging
from app.services.format_comment import format_comment

logger = logging.getLogger(__name__)


class CRUDComment:
    # create
    def create_comment(self, db: Session, new_comment: CommentCreate, user_id: int):
        try:
            comment = Comments(
                comment=new_comment.comment,
                post_id=new_comment.post_id,
                parent_comment_id=new_comment.parent_comment_id or None,
                user_id=user_id,
            )
            db.add(comment)
            db.flush()
            db.commit()
            logger.info("Commented Successfully")
            return comment
        except IntegrityError as e:
            db.rollback()
            logger.error(f"error creating comment: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"error creating comment: {str(e)}")
            raise DatabaseError("Failed to create comment")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating comment: {str(e)}")

    # get all post comment
    def get_comments_by_post_id(self, db: Session, post_id: int):
        try:
            top_level_comments = (
                db.query(Comments)
                .filter(Comments.post_id == post_id, Comments.parent_comment_id == None)
                .all()
            )
            if not top_level_comments:
                raise NotFoundError("No Comments Available")

            formatted_comments = [
                format_comment(comment) for comment in top_level_comments
            ]
            return formatted_comments
        except SQLAlchemyError as e:
            logger.error(f"Error fetching comments by post id: {str(e)}")
            raise DatabaseError("Failed to fetch comments post by id")


crud_comment = CRUDComment()
