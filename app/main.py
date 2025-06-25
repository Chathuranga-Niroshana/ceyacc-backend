from fastapi import FastAPI
from app.db.session import SessionLocal
from app.db.init_db import init_default_roles, init_score_levels

app = FastAPI()


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    init_default_roles(db)
    init_score_levels(db)
    db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to CeyAcc backend "}
