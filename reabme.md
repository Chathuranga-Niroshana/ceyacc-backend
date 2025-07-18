alembic revision --autogenerate -m "db new commit"
alembic upgrade head
uvicorn app.main:app --reload