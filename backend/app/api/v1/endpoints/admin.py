import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.v1.deps import CurrentUser, SessionDep
from app.models.domain import Domain, Course
from app.models.lesson import Lesson
from app.models.user import User
from app.schemas.admin import (
    CourseAdminResponse,
    CourseCreate,
    CourseUpdate,
    DomainAdminResponse,
    DomainCreate,
    DomainUpdate,
    LessonAdminResponse,
    LessonCreate,
    LessonUpdate,
)

router = APIRouter()


def require_admin(current_user: CurrentUser) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user


AdminDep = Depends(require_admin)


# ─── Domains ─────────────────────────────────────────────────────────────────

@router.get("/domains", response_model=list[DomainAdminResponse])
def list_domains(session: SessionDep, _: User = AdminDep):
    domains = session.exec(select(Domain).order_by(Domain.order_index)).all()
    return [DomainAdminResponse(**d.model_dump()) for d in domains]


@router.post("/domains", response_model=DomainAdminResponse, status_code=status.HTTP_201_CREATED)
def create_domain(body: DomainCreate, session: SessionDep, _: User = AdminDep):
    existing = session.exec(select(Domain).where(Domain.slug == body.slug)).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Domain slug '{body.slug}' already exists")
    domain = Domain(**body.model_dump())
    session.add(domain)
    session.commit()
    session.refresh(domain)
    return DomainAdminResponse(**domain.model_dump())


@router.put("/domains/{domain_id}", response_model=DomainAdminResponse)
def update_domain(domain_id: uuid.UUID, body: DomainUpdate, session: SessionDep, _: User = AdminDep):
    domain = session.get(Domain, domain_id)
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(domain, field, value)
    session.add(domain)
    session.commit()
    session.refresh(domain)
    return DomainAdminResponse(**domain.model_dump())


# ─── Courses ─────────────────────────────────────────────────────────────────

@router.get("/courses", response_model=list[CourseAdminResponse])
def list_courses(session: SessionDep, _: User = AdminDep):
    courses = session.exec(select(Course).order_by(Course.order_index)).all()
    result = []
    for c in courses:
        domain = session.get(Domain, c.domain_id)
        result.append(CourseAdminResponse(
            **c.model_dump(),
            domain_name=domain.name if domain else "",
        ))
    return result


@router.post("/courses", response_model=CourseAdminResponse, status_code=status.HTTP_201_CREATED)
def create_course(body: CourseCreate, session: SessionDep, _: User = AdminDep):
    existing = session.exec(select(Course).where(Course.slug == body.slug)).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Course slug '{body.slug}' already exists")
    domain = session.get(Domain, body.domain_id)
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    course = Course(**body.model_dump())
    session.add(course)
    session.commit()
    session.refresh(course)
    return CourseAdminResponse(**course.model_dump(), domain_name=domain.name)


@router.put("/courses/{course_id}", response_model=CourseAdminResponse)
def update_course(course_id: uuid.UUID, body: CourseUpdate, session: SessionDep, _: User = AdminDep):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(course, field, value)
    session.add(course)
    session.commit()
    session.refresh(course)
    domain = session.get(Domain, course.domain_id)
    return CourseAdminResponse(**course.model_dump(), domain_name=domain.name if domain else "")


# ─── Lessons ─────────────────────────────────────────────────────────────────

@router.get("/lessons", response_model=list[LessonAdminResponse])
def list_lessons(session: SessionDep, _: User = AdminDep, course_id: uuid.UUID | None = None):
    query = select(Lesson)
    if course_id:
        query = query.where(Lesson.course_id == course_id)
    lessons = session.exec(query.order_by(Lesson.order_index)).all()
    result = []
    for l in lessons:
        course = session.get(Course, l.course_id)
        domain = session.get(Domain, course.domain_id) if course else None
        result.append(LessonAdminResponse(
            id=l.id,
            course_id=l.course_id,
            course_name=course.name if course else "",
            domain_name=domain.name if domain else "",
            title=l.title,
            content_type=l.content_type,
            order_index=l.order_index,
            estimated_minutes=l.estimated_minutes,
            is_active=l.is_active,
        ))
    return result


@router.get("/lessons/{lesson_id}")
def get_lesson_detail(lesson_id: uuid.UUID, session: SessionDep, _: User = AdminDep):
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.post("/lessons", status_code=status.HTTP_201_CREATED)
def create_lesson(body: LessonCreate, session: SessionDep, _: User = AdminDep):
    course = session.get(Course, body.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    lesson = Lesson(**body.model_dump())
    session.add(lesson)
    session.commit()
    session.refresh(lesson)
    return lesson


@router.put("/lessons/{lesson_id}")
def update_lesson(lesson_id: uuid.UUID, body: LessonUpdate, session: SessionDep, _: User = AdminDep):
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(lesson, field, value)
    session.add(lesson)
    session.commit()
    session.refresh(lesson)
    return lesson
