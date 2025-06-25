from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.user import Student


def update_student_grades(db: Session):
    today = datetime.now(timezone.utc)
    if today.month != 1 or today.date != 1:
        return

    students = db.query(Student).filter(Student.is_completed == False).all()

    for student in students:
        if student.grade is None:
            student.grade = 1

        if student.grade < 13:
            student.grade += 1
            print(f"Incremented grade for student {student.id} to {student.grade}")
        else:
            student.is_completed = True
            print(f"Marked student {student.id} as completed")

    db.commit()
