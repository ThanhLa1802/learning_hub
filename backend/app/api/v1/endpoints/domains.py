import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, status

from app.api.v1.deps import CurrentUser, SessionDep
from app.repositories import domain as domain_crud
from app.repositories import lesson as lesson_crud
from app.schemas.domain import CourseResponse, DomainResponse, DomainWithCoursesResponse
from app.schemas.lesson import LessonSummaryResponse
from app.schemas.scenario import ScenarioCategoryResponse
from app.utils.translation import apply_lang

router = APIRouter()


@router.get("/", response_model=list[DomainWithCoursesResponse])
def list_domains(session: SessionDep, _: CurrentUser, lang: str = "en"):
    domains = domain_crud.get_all_active(session)
    result = []
    for domain in domains:
        courses = domain_crud.get_courses_by_domain(session, domain.id)
        resp = DomainWithCoursesResponse.model_validate(domain)
        apply_lang(resp, domain.translations, lang)
        resp.courses = []
        for c in courses:
            cr = CourseResponse.model_validate(c)
            apply_lang(cr, c.translations, lang)
            resp.courses.append(cr)
        result.append(resp)
    return result


@router.get("/{slug}", response_model=DomainWithCoursesResponse)
def get_domain(slug: str, session: SessionDep, _: CurrentUser, lang: str = "en"):
    domain = domain_crud.get_by_slug(session, slug)
    if not domain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found")
    courses = domain_crud.get_courses_by_domain(session, domain.id)
    response = DomainWithCoursesResponse.model_validate(domain)
    apply_lang(response, domain.translations, lang)
    response.courses = []
    for c in courses:
        cr = CourseResponse.model_validate(c)
        apply_lang(cr, c.translations, lang)
        response.courses.append(cr)
    return response


@router.get("/{slug}/topics", response_model=list[ScenarioCategoryResponse])
def get_domain_topics(slug: str, session: SessionDep, _: CurrentUser, lang: str = "en"):
    """Return all scenario categories (topics) belonging to this domain."""
    domain = domain_crud.get_by_slug(session, slug)
    if not domain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found")
    courses = domain_crud.get_courses_by_domain(session, domain.id)
    course_ids = [c.id for c in courses]
    categories = domain_crud.get_categories_by_course_ids(session, course_ids)
    result = []
    for cat in categories:
        resp = ScenarioCategoryResponse.model_validate(cat)
        apply_lang(resp, cat.translations, lang)
        result.append(resp)
    return result


@router.get("/{slug}/lessons", response_model=list[LessonSummaryResponse])
def get_domain_lessons(slug: str, session: SessionDep, current_user: CurrentUser, category_id: Optional[uuid.UUID] = None, lang: str = "en"):
    """Return lessons for a domain, optionally filtered by category."""
    domain = domain_crud.get_by_slug(session, slug)
    if not domain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found")
    if category_id:
        lessons = lesson_crud.get_by_category(session, category_id)
    else:
        courses = domain_crud.get_courses_by_domain(session, domain.id)
        lessons = []
        for course in courses:
            lessons.extend(lesson_crud.get_by_course(session, course.id))
    completed_ids = lesson_crud.get_user_completed_ids(session, current_user.id)
    result = []
    for l in lessons:
        resp = LessonSummaryResponse.model_validate(l)
        resp.is_completed = l.id in completed_ids
        apply_lang(resp, l.translations, lang)
        result.append(resp)
    return result
