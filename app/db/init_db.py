from sqlalchemy.orm import Session
from app.models.system import UserRoles, ScoreLevels


def init_default_roles(db: Session):
    default_roles = [
        {"id": 1, "name": "student"},
        {"id": 2, "name": "teacher"},
        {"id": 3, "name": "admin"},
    ]
    for role in default_roles:
        exists = db.query(UserRoles).filter_by(id=role["id"]).first()
        if not exists:
            db.add(UserRoles(**role))
    db.commit()


def init_score_levels(db: Session):
    default_levels = [
        {
            "id": 1,
            "name": "Novice Scout",
            "image": "https://img.icons8.com/color/96/compass.png",
            "max_limit": 100,
        },
        {
            "id": 2,
            "name": "Apprentice",
            "image": "https://img.icons8.com/color/96/open-book--v1.png",
            "max_limit": 250,
        },
        {
            "id": 3,
            "name": "Code Knight",
            "image": "https://img.icons8.com/color/96/medieval-crown.png",
            "max_limit": 500,
        },
        {
            "id": 4,
            "name": "Tech Ranger",
            "image": "https://img.icons8.com/color/96/worldwide-location.png",
            "max_limit": 800,
        },
        {
            "id": 5,
            "name": "Quiz Wizard",
            "image": "https://img.icons8.com/color/96/magic-wand.png",
            "max_limit": 1200,
        },
        {
            "id": 6,
            "name": "Knowledge Ninja",
            "image": "https://img.icons8.com/color/96/ninja.png",
            "max_limit": 1600,
        },
        {
            "id": 7,
            "name": "Mastermind",
            "image": "https://img.icons8.com/color/96/brain.png",
            "max_limit": 2200,
        },
        {
            "id": 8,
            "name": "Elite Scholar",
            "image": "https://img.icons8.com/color/96/graduation-cap.png",
            "max_limit": 3000,
        },
        {
            "id": 9,
            "name": "Legend",
            "image": "https://img.icons8.com/color/96/trophy.png",
            "max_limit": 4000,
        },
        {
            "id": 10,
            "name": "Grandmaster",
            "image": "https://img.icons8.com/color/96/medal2.png",
            "max_limit": 6000,
        },
    ]
    for level in default_levels:
        exists = db.query(ScoreLevels).filter_by(id=level["id"]).first()
        if not exists:
            db.add(ScoreLevels(**level))
    db.commit()
