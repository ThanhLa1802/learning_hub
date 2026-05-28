import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, status

from app.api.v1.deps import CurrentUser, SessionDep
from app.repositories import domain as domain_crud
from app.repositories import lesson as lesson_crud
from app.repositories import progress as progress_crud
from app.repositories import quiz as quiz_crud
from app.models.domain import Course
from app.models.lesson import Lesson
from app.schemas.lesson import AIExplainRequest, AIExplainResponse, LessonResponse, LessonSummaryResponse
from app.services import lesson_service
from app.utils.translation import apply_lang

router = APIRouter()


def _get_domain_id_for_lesson(session, lesson: Lesson) -> Optional[uuid.UUID]:
    course = session.get(Course, lesson.course_id)
    return course.domain_id if course else None


@router.get("/", response_model=list[LessonSummaryResponse])
def list_lessons(
    session: SessionDep,
    _: CurrentUser,
    category_id: Optional[uuid.UUID] = None,
    course_id: Optional[uuid.UUID] = None,
):
    if category_id:
        lessons = lesson_crud.get_by_category(session, category_id)
    elif course_id:
        lessons = lesson_crud.get_by_course(session, course_id)
    else:
        return []
    return [LessonSummaryResponse.model_validate(l) for l in lessons]


@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: uuid.UUID, session: SessionDep, current_user: CurrentUser, lang: str = "en"):
    lesson = lesson_crud.get_by_id(session, lesson_id)
    if not lesson or not lesson.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    quiz = quiz_crud.get_by_lesson(session, lesson_id)
    response = LessonResponse.model_validate(lesson)
    response.quiz_id = quiz.id if quiz else None
    response.is_completed = lesson_crud.is_completed(session, current_user.id, lesson_id)
    response.quiz_passed = (
        quiz_crud.has_passing_attempt(session, current_user.id, quiz.id)
        if quiz else True
    )
    next_lesson = lesson_crud.get_next_lesson(session, lesson)
    response.next_lesson_id = next_lesson.id if next_lesson else None
    apply_lang(response, lesson.translations, lang)
    return response


@router.post("/{lesson_id}/explain", response_model=AIExplainResponse)
def ai_explain(lesson_id: uuid.UUID, request: AIExplainRequest, session: SessionDep, _: CurrentUser, lang: str = "en"):
    lesson = lesson_crud.get_by_id(session, lesson_id)
    if not lesson or not lesson.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    result = lesson_service.explain_concept(lesson, request.question, lang)
    return AIExplainResponse(**result)


@router.post("/{lesson_id}/complete", status_code=status.HTTP_204_NO_CONTENT)
def mark_lesson_complete(lesson_id: uuid.UUID, session: SessionDep, current_user: CurrentUser):
    lesson = lesson_crud.get_by_id(session, lesson_id)
    if not lesson or not lesson.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    quiz = quiz_crud.get_by_lesson(session, lesson_id)
    if quiz and not quiz_crud.has_passing_attempt(session, current_user.id, quiz.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must pass the quiz with a score of 80% or higher before marking this lesson complete.",
        )
    lesson_crud.mark_complete(session, current_user.id, lesson_id)
    domain_id = _get_domain_id_for_lesson(session, lesson)
    if domain_id:
        progress_crud.increment_lessons(session, current_user.id, domain_id)
