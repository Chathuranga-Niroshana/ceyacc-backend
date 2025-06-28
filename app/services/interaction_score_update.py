from app.models.user import User
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)


def update_user_score(db: Session, value: int, user_id: int):
    try:
        user = db.get(User, user_id)
        if not user:
            return None
        user.system_score += value
        db.commit()
        db.refresh(user)
        logger.info("score updated")
        return user.system_score
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating score: {str(e)}")
        return None
