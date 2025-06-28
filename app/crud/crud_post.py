from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostResponse
from typing import Optional, List
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.core.exceptions import (
    DatabaseError,
    ValidationError,
    NotFoundError,
    AuthorizationError,
)
import logging

logger = logging.getLogger(__name__)


class CRUDPost:
    # create
    def create_post(self, db: Session, new_post: PostCreate, user_id: int):
        try:
            post = Post(
                media_link=new_post.media_link,
                media_type=new_post.media_type,
                title=new_post.title,
                description=new_post.description,
                is_public=new_post.is_public,
                user_id=user_id,
            )
            db.add(post)
            db.flush()
            db.commit()
            logger.info("Post created successfully")
            return post
        except IntegrityError as e:
            db.rollback()
            logger.error(f"error creating post: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"error creating post: {str(e)}")
            raise DatabaseError("Failed to create post")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating post: {str(e)}")
            raise DatabaseError("An unexpected error occurred")

    # get by id
    def get_post_by_id(self, db: Session, post_id: int, user_id: int):
        try:
            post = db.get(Post, post_id)
            if not post:
                raise NotFoundError("Post not found")

            if not post.is_public and post.user_id != user_id:
                raise AuthorizationError("Not Authorized to view")

            comments_count = len(post.comment)
            reaction_count = len(post.post_reaction)
            avg_ratings = (
                sum(r.ratings for r in post.post_rating) / len(post.post_rating)
                if post.post_rating
                else 0.0
            )
            posted_user = {
                "id": post.user_id,
                "name": post.user.name,
                "image": post.user.image or None,
            }

            return PostResponse(
                id=post.id,
                media_type=post.media_type,
                media_link=post.media_link,
                title=post.title,
                description=post.description,
                is_public=post.is_public,
                user=posted_user,
                created_at=post.created_at,
                updated_at=post.updated_at,
                comments_number=comments_count or 0,
                reaction_number=reaction_count or 0,
                post_ratings=avg_ratings,
            )

        except SQLAlchemyError as e:
            logger.error(f"Error fetching post by id: {str(e)}")
            raise DatabaseError("Failed to fetch post by id")


crud_post = CRUDPost()
