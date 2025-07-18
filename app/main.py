import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.db.session import SessionLocal
from app.db.init_db import (
    init_default_roles,
    init_score_levels,
    init_default_reaction_types,
)
from app.utils.scheduler import start_scheduler
from app.middleware.auth_middleware import AuthMiddleware
from app.core.exceptions import (
    NotFoundError,
    DatabaseError,
    AuthenticationError,
    ValidationError,
    AuthorizationError,
)
from app.core.config import settings


# routes
from app.api.v1.routes import auth
from app.api.v1.routes import user
from app.api.v1.routes import post
from app.api.v1.routes import comment
from app.api.v1.routes import post_react
from app.api.v1.routes import event
from app.api.v1.routes import quiz
from app.api.v1.routes import exam_paper
from app.api.v1.routes import course

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        init_default_roles(db)
        init_score_levels(db)
        init_default_reaction_types(db)
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
app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.CLIENT_URL,
    allow_origins="http://localhost:5173",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(post.router, prefix="/api")
app.include_router(comment.router, prefix="/api")
app.include_router(post_react.router, prefix="/api")
app.include_router(event.router, prefix="/api")
app.include_router(quiz.router, prefix="/api")
app.include_router(exam_paper.router, prefix="/api")
app.include_router(course.router, prefix="/api")

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
async def authorization_exception_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )


@app.exception_handler(AuthorizationError)
async def auth_exception_handler(request: Request, exc: AuthorizationError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Validation failed", "detail": str(exc)},
    )


@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Welcome to CeyAcc backend "}
