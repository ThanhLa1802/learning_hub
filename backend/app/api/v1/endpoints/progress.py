from fastapi import APIRouter
from sqlmodel import select, func

from app.api.v1.deps import CurrentUser, SessionDep
from app.models.domain import Course
from app.models.lesson import Lesson
from app.repositories import progress as progress_crud
from app.schemas.progress import UserDomainProgressResponse, UserProgressResponse

router = APIRouter()


@router.get("/", response_model=UserProgressResponse)
def get_progress(session: SessionDep, current_user: CurrentUser):
    items = progress_crud.get_all_for_user(session, current_user.id)
    domain_progresses = []
    for prog, domain in items:
        total = session.exec(
            select(func.count(Lesson.id))
            .join(Course, Lesson.course_id == Course.id)
            .where(Course.domain_id == domain.id, Lesson.is_active == True)
        ).one()
        domain_progresses.append(
            UserDomainProgressResponse(
                domain_id=domain.id,
                domain_name=domain.name,
                sessions_completed=prog.sessions_completed,
                lessons_completed=prog.lessons_completed,
                total_lessons=total,
                quizzes_taken=prog.quizzes_taken,
                avg_quiz_score=prog.avg_quiz_score,
                last_activity_at=prog.last_activity_at,
            )
        )
    return UserProgressResponse(domains=domain_progresses)
