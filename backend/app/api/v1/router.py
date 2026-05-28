from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, domains, lessons, progress, quizzes, scenarios, sessions, users

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
router.include_router(domains.router, prefix="/domains", tags=["domains"])
router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
router.include_router(progress.router, prefix="/progress", tags=["progress"])
router.include_router(admin.router, prefix="/admin", tags=["admin"])
