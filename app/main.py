from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.db.session import SessionLocal
from app.db.init_db import init_default_roles, init_score_levels
from app.utils.scheduler import start_scheduler
import logging

# routes
from app.api.v1.routes import auth
from app.api.v1.routes import user


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        init_default_roles(db)
        init_score_levels(db)
        start_scheduler()
        print("[Startup] Initialized default roles, score levels, and scheduler.")
        yield
    except Exception as e:
        logger.error(f"Startup Error: {str(e)}")
        yield
    finally:
        db.close()


app = FastAPI(
    title="CeyAcc API",
    version="1.0.0",
    description="Backend API for CeyAcc — A social media platform for school students and teachers to collaborate ",
    lifespan=lifespan,
)

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Validation failed",
            "errors": exc.errors(),
            "body": exc.body,
        },
    )


@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Welcome to CeyAcc backend "}
