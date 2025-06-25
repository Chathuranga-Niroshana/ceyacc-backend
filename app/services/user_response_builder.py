from app.schemas.user import UserResponse, ScoreLevel as ScoreLevelSchema
from app.models.system import ScoreLevels
from sqlalchemy.orm import Session
from app.models.user import User as UserModel


def build_user_response(user: UserModel, db: Session) -> UserResponse:
    score_levels = db.query(ScoreLevels).order_by(ScoreLevels.max_limit.asc()).all()
    level_data = None
    for level in score_levels:
        if user.system_score <= level.max_limit:
            level_data = level
            break
    if not level_data and score_levels:
        level_data = score_levels[-1]

    level_schema = ScoreLevelSchema.from_orm(level_data) if level_data else None

    return UserResponse(
        id=user.id,
        image=user.image,
        cover_image=user.cover_image,
        name=user.name,
        bio=user.bio,
        email=user.email,
        mobile_no=user.mobile_no,
        dob=user.dob,
        system_score=user.system_score,
        school_name=user.school_name,
        address_line_one=user.address_line_one,
        city=user.city,
        province=user.province,
        sex=user.sex,
        nic=user.nic,
        is_verified=user.is_verified,
        role_id=user.role_id,
        created_at=user.created_at,
        updated_at=user.updated_at,
        teacher=user.teacher,
        student=user.student,
        level=level_schema,
    )
