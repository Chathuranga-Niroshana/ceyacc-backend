from app.db.session import SessionLocal
from app.services.grade_updater import update_student_grades


def main():
    db = SessionLocal()
    try:
        update_student_grades(db)
        print("Student grades updated successfully")
    except Exception as e:
        print("Failed to update student grades: ", e)
    finally:
        db.close()


if __name__ == "__main__":
    main()
