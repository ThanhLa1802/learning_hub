from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlmodel import SQLModel

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.database import engine

# Import all models to register them with SQLModel metadata (order matters for FK resolution)
from app.models import (  # noqa: F401
    Domain, Course,
    User,
    ScenarioCategory, Scenario,
    PracticeSession, SessionMessage,
    Lesson, Quiz, QuizQuestion,
    UserQuizAttempt, UserLessonProgress, UserDomainProgress,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    # Add course_id FK to existing scenario_categories table (idempotent)
    with engine.connect() as conn:
        conn.execute(text(
            "ALTER TABLE scenario_categories "
            "ADD COLUMN IF NOT EXISTS course_id UUID REFERENCES courses(id)"
        ))
        conn.commit()
    from app.db.seed import seed_database
    from sqlmodel import Session
    with Session(engine) as session:
        seed_database(session)
    yield


app = FastAPI(
    title="English for IT Developers API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
