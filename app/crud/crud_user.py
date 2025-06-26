from sqlalchemy.orm import Session
from app.models.user import User, Teacher, Student
from app.schemas.user import UserFullCreate, UserUpdate, User as UserSchema
from typing import Optional, List
from app.utils.security import hash_password
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.constants.roles import ROLE_TEACHER, ROLE_STUDENT
from app.core.exceptions import DatabaseError, ValidationError, NotFoundError
import logging

logger = logging.getLogger(__name__)


class CRUDUser:

    # register
    def create_user(self, db: Session, user_in: UserFullCreate) -> UserSchema:
        try:
            if user_in.role_id == ROLE_TEACHER and not user_in.teacher:
                raise ValidationError("Teacher data is required")
            elif user_in.role_id == ROLE_STUDENT and not user_in.student:
                raise ValidationError("Student data is required")
            existing_user = self._check_existing_user(db, user_in.email, user_in.nic)
            if existing_user:
                raise ValidationError("User with this email or NIC already exists")
            hashed_password = hash_password(user_in.password)
            user = User(
                image=user_in.image,
                cover_image=user_in.cover_image,
                name=user_in.name,
                bio=user_in.bio,
                email=user_in.email,
                password=hashed_password,
                mobile_no=user_in.mobile_no,
                dob=user_in.dob,
                school_name=user_in.school_name,
                address_line_one=user_in.address_line_one,
                city=user_in.city,
                province=user_in.province,
                sex=user_in.sex,
                nic=user_in.nic,
                is_verified=user_in.is_verified or False,
                role_id=user_in.role_id,
            )
            db.add(user)
            db.flush()
            if user_in.teacher:
                teacher = Teacher(
                    user_id=user.id,
                    subjects_taught=user_in.teacher.subjects_taught,
                    teaching_experience=user_in.teacher.teaching_experience,
                )
                db.add(teacher)
            if user_in.student:
                student = Student(
                    user_id=user.id, grade=user_in.student.grade, is_completed=False
                )
                db.add(student)
            db.commit()
            db.refresh(user)
            logger.info(f"User created successfully: {user.email}")
            return user

        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity error creating user: {str(e)}")
            raise ValidationError("User with email or nic already exists")
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error creating user: {str(e)}")
            raise DatabaseError("Failed to create user")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating user: {str(e)}")
            raise DatabaseError("An unexpected error occurred")

    # get user by id
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[UserSchema]:
        try:
            return db.get(User, user_id)
        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by id: {str(e)}")
            raise DatabaseError("Failed to fetch user by id")

    # get user by email
    def get_user_by_email(self, db: Session, email: str) -> Optional[UserSchema]:
        try:
            clean_email = email.lower().strip()
            return db.query(User).filter(User.email == clean_email).first()

        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by email: {str(e)}")
            raise DatabaseError("Failed to fetch user")

    # get user by nic
    def get_user_by_nic(self, db: Session, nic: str) -> Optional[UserSchema]:
        try:
            return db.query(User).filter(User.nic == nic.strip()).first()

        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by nic: {str(e)}")
            raise DatabaseError("Failed to fetch user")

    def _check_existing_user(self, db: Session, email: str, nic: str) -> Optional[User]:
        existing_email = self.get_user_by_email(db, email)
        if existing_email:
            return existing_email
        existing_nic = self.get_user_by_nic(db, nic)
        if existing_nic:
            return existing_nic
        return None


crud_user = CRUDUser()
