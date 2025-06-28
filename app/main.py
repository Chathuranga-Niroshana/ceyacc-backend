import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.db.session import SessionLocal
from app.db.init_db import init_default_roles, init_score_levels
from app.utils.scheduler import start_scheduler
from app.middleware.auth_middleware import AuthMiddleware
from app.core.exceptions import (
    NotFoundError,
    DatabaseError,
    AuthenticationError,
    ValidationError,
)


# routes
from app.api.v1.routes import auth
from app.api.v1.routes import user
from app.api.v1.routes import post

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


app.add_middleware(AuthMiddleware)
app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(post.router, prefix="/api")


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )


@app.exception_handler(DatabaseError)
async def database_exception_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


@app.exception_handler(AuthenticationError)
async def auth_exception_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )


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
