import logging
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.schemas.events import (
    EventCreate,
    EventInterestResponse,
    EventInterestsCreate,
    EventResponse,
)
from app.crud.crud_event import crud_events
from app.core.exceptions import (
    ValidationError,
    DatabaseError,
    NotFoundError,
)
from app.db.deps import get_db
from app.constants.score_update_values import SCORE_UPDATE_VALUES
from app.services.interaction_score_update import update_user_score
from typing import List

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/events", tags=["Events"])


# create event
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_event(
    request: Request, new_event: EventCreate, db: Session = Depends(get_db)
):
    try:
        user = request.state.user
        event = crud_events.create_event(db=db, new_event=new_event, user_id=user.id)
        update_user_score(
            db=db, value=SCORE_UPDATE_VALUES["CREATE_EVENT"], user_id=user.id
        )
        logger.info("Event Created")
        return {"success": True, "event": event}
    except ValidationError as e:
        logger.warning(f"Validation error in create: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error in create: {str(e)}")
        raise DatabaseError("Unexpected error occurred while creating")


# get all active events
@router.get(
    "/get_active_events",
    response_model=List[EventResponse],
    status_code=status.HTTP_200_OK,
)
async def get_active_events(db: Session = Depends(get_db)):
    try:
        events = crud_events.get_all_active_events(db=db)
        if not events:
            raise NotFoundError("Events Not Available")
        return events
    except NotFoundError as e:
        logger.warning(str(e))
        raise NotFoundError(str(e))
    except ValidationError as e:
        logger.warning(f"Validation error : {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error : {str(e)}")
        raise DatabaseError("Unexpected error occurred ")


# get all inactive events
@router.get(
    "/get_inactive_events",
    response_model=List[EventResponse],
    status_code=status.HTTP_200_OK,
)
async def get_inactive_events(db: Session = Depends(get_db)):
    try:
        events = crud_events.get_all_inactive_events(db=db)
        if not events:
            raise NotFoundError("Events Not Available")
        return events
    except NotFoundError as e:
        logger.warning(str(e))
        raise NotFoundError(str(e))
    except ValidationError as e:
        logger.warning(f"Validation error : {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error : {str(e)}")
        raise DatabaseError("Unexpected error occurred ")


# get event by id
@router.get(
    "/get/{event_id}",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
)
async def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    try:
        event = crud_events.get_event_by_id(db=db, event_id=event_id)
        if not event:
            raise NotFoundError("Events Not Available")
        return event
    except ValidationError as e:
        logger.warning(f"Validation error : {str(e)}")
        raise ValidationError(str(e))
    except NotFoundError as e:
        logger.warning(str(e))
        raise NotFoundError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error : {str(e)}")
        raise DatabaseError("Unexpected error occurred ")


# create event interest
@router.post("/interest/create/{event_id}", status_code=status.HTTP_201_CREATED)
async def create_event(
    request: Request,
    new_interest: EventInterestsCreate,
    event_id: int,
    db: Session = Depends(get_db),
):
    try:
        user = request.state.user
        event_interest = crud_events.create_event_interest(
            db=db, new_interest=new_interest, event_id=event_id, user_id=user.id
        )
        update_user_score(
            db=db, value=SCORE_UPDATE_VALUES["INTEREST_EVENT"], user_id=user.id
        )
        logger.info("Event Interest Created")
        return {"success": True, "event_interest": event_interest}
    except ValidationError as e:
        logger.warning(f"Validation error in create: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error in create: {str(e)}")
        raise DatabaseError("Unexpected error occurred while creating")


# get event interests by id
@router.get(
    "/interest/get/{event_id}",
    response_model=List[EventInterestResponse],
    status_code=status.HTTP_200_OK,
)
async def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    try:
        event_interests = crud_events.get_event_interest_by_event_id(
            db=db, event_id=event_id
        )
        if not event_interests:
            raise NotFoundError("Events Not Available")
        return event_interests
    except NotFoundError as e:
        logger.warning(str(e))
        raise NotFoundError(str(e))
    except ValidationError as e:
        logger.warning(f"Validation error : {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Unexpected error : {str(e)}")
        raise DatabaseError("Unexpected error occurred ")
