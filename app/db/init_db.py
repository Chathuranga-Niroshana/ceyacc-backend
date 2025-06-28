from sqlalchemy.orm import Session
from app.models.system import UserRoles, ScoreLevels, ReactionTypes
from app.constants.roles import DEFAULT_ROLES_FOR_DB
from app.constants.user_levels import DEFAULT_USER_LEVELS
from app.constants.reaction_types import DEFAULT_REACTION_TYPES


def init_model_defaults(db: Session, model, default_data: list):
    existing_ids = {row.id for row in db.query(model.id).all()}
    new_entries = [
        model(**item) for item in default_data if item["id"] not in existing_ids
    ]

    if new_entries:
        db.add_all(new_entries)
        db.commit()


def init_default_roles(db: Session):
    init_model_defaults(db, UserRoles, DEFAULT_ROLES_FOR_DB)


def init_score_levels(db: Session):
    init_model_defaults(db, ScoreLevels, DEFAULT_USER_LEVELS)


def init_default_reaction_types(db: Session):
    init_model_defaults(db, ReactionTypes, DEFAULT_REACTION_TYPES)
