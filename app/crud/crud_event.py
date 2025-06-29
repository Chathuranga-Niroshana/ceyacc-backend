import logging
from app.models.events import Event, EventInterests
from app.schemas.events import (
    EventCreate,
    EventInterestsCreate,
    EventInterestResponse,
    EventResponse,
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.core.exceptions import (
    DatabaseError,
    ValidationError,
    NotFoundError,
)
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class CRUDEvents:
    # create event
    def create_event(self, db: Session, new_event: EventCreate, user_id: int):
        try:
            event = Event(
                title=new_event.title,
                date_time=new_event.date_time,
                location=new_event.location,
                description=new_event.description,
                media_url_one=new_event.media_url_one,
                media_url_two=new_event.media_url_two,
                media_url_three=new_event.media_url_three,
                media_url_four=new_event.media_url_four,
                media_url_five=new_event.media_url_five,
                user_id=user_id,
            )
            db.add(event)
            db.flush()
            db.commit()
            db.refresh(event)
            logger.info("Created Successfully")
            return event
        except IntegrityError as e:
            db.rollback()
            logger.error(f"error: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"error: {str(e)}")
            raise DatabaseError("Failed to react")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error: {str(e)}")

    # get all active events
    def get_all_active_events(self, db: Session):
        try:
            events = (
                db.query(Event)
                .filter(Event.date_time >= datetime.now(tz=timezone.utc))
                .all()
            )
            if not events:
                raise NotFoundError("No Events Available")

            formatted_events = []
            for event in events:
                formatted_user = {
                    "id": event.user_id,
                    "name": event.user.name,
                    "image": event.user.image or None,
                }

                formatted_event = EventResponse(
                    id=event.id,
                    title=event.title,
                    date_time=event.date_time,
                    location=event.location,
                    description=event.description,
                    media_url_one=event.media_url_one,
                    media_url_two=event.media_url_two,
                    media_url_three=event.media_url_three,
                    media_url_four=event.media_url_four,
                    media_url_five=event.media_url_five,
                    created_at=event.created_at,
                    user=formatted_user,
                )
                formatted_events.append(formatted_event)
            return formatted_events
        except IntegrityError as e:
            logger.error(f"error: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            logger.error(f"error: {str(e)}")
            raise DatabaseError("Failed to react")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

    # get all inactive events
    def get_all_inactive_events(self, db: Session):
        try:
            events = (
                db.query(Event)
                .filter(Event.date_time <= datetime.now(tz=timezone.utc))
                .all()
            )
            if not events:
                raise NotFoundError("No Events Available")

            formatted_events = []
            for event in events:
                formatted_user = {
                    "id": event.user_id,
                    "name": event.user.name,
                    "image": event.user.image or None,
                }

                formatted_event = EventResponse(
                    id=event.id,
                    title=event.title,
                    date_time=event.date_time,
                    location=event.location,
                    description=event.description,
                    media_url_one=event.media_url_one,
                    media_url_two=event.media_url_two,
                    media_url_three=event.media_url_three,
                    media_url_four=event.media_url_four,
                    media_url_five=event.media_url_five,
                    created_at=event.created_at,
                    user=formatted_user,
                )
                formatted_events.append(formatted_event)
            return formatted_events
        except IntegrityError as e:
            logger.error(f"error: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            logger.error(f"error: {str(e)}")
            raise DatabaseError("Failed to react")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

    # get event by id
    def get_event_by_id(self, db: Session, event_id: int):
        try:
            event = db.get(Event, event_id)
            if not event:
                raise NotFoundError("No Events Available")
            formatted_user = {
                "id": event.user_id,
                "name": event.user.name,
                "image": event.user.image or None,
            }
            formatted_event = EventResponse(
                id=event.id,
                title=event.title,
                date_time=event.date_time,
                location=event.location,
                description=event.description,
                media_url_one=event.media_url_one,
                media_url_two=event.media_url_two,
                media_url_three=event.media_url_three,
                media_url_four=event.media_url_four,
                media_url_five=event.media_url_five,
                created_at=event.created_at,
                user=formatted_user,
            )
            return formatted_event
        except IntegrityError as e:
            logger.error(f"error: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            logger.error(f"error: {str(e)}")
            raise DatabaseError("Failed to react")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

    # create event interest
    def create_event_interest(
        self,
        db: Session,
        new_interest: EventInterestsCreate,
        event_id: int,
        user_id: int,
    ):
        try:
            existing_interest = (
                db.query(EventInterests)
                .filter(
                    EventInterests.event_id == event_id,
                    EventInterests.user_id == user_id,
                )
                .first()
            )
            if existing_interest:
                existing_interest.interest_type = new_interest.interest_type
                db.commit()
                db.refresh(existing_interest)
                logger.info("interest updated")
                return None
            event_interest = EventInterests(
                interest_type=new_interest.interest_type,
                user_id=user_id,
                event_id=event_id,
            )
            db.add(event_interest)
            db.flush()
            db.commit()
            db.refresh(event_interest)
            logger.info("Created Successfully")
            return event_interest
        except IntegrityError as e:
            db.rollback()
            logger.error(f"error: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"error: {str(e)}")
            raise DatabaseError("Failed to react")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error: {str(e)}")

    # get event by id
    def get_event_interest_by_event_id(self, db: Session, event_id: int):
        try:
            event = db.get(Event, event_id)
            if not event:
                raise NotFoundError("No Events Available")

            interests = (
                db.query(EventInterests)
                .filter(EventInterests.event_id == event_id)
                .all()
            )
            if not interests:
                raise NotFoundError("No Events Interests Available")

            formatted_interests = []

            for interest in interests:
                formatted_user = {
                    "id": interest.user_id,
                    "name": interest.user.name,
                    "image": interest.user.image or None,
                }
                formatted_interest = EventInterestResponse(
                    id=interest.id,
                    interest_type=interest.interest_type,
                    created_at=interest.created_at,
                    user=formatted_user,
                )
                formatted_interests.append(formatted_interest)

            return formatted_interests
        except IntegrityError as e:
            logger.error(f"error: {str(e)}")
            raise ValidationError(str(e))
        except SQLAlchemyError as e:
            logger.error(f"error: {str(e)}")
            raise DatabaseError("Failed to react")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")


crud_events = CRUDEvents()
