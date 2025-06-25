from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.grade_updater import update_student_grades


def run_update():
    db = SessionLocal()
    try:
        update_student_grades(db)
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_update, "cron", month=1, day=1, hour=0, minute=0)
    scheduler.start()
    print("Scheduler started for yearly grade updates.")
