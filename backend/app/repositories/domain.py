import uuid
from typing import Optional

from sqlmodel import Session, select

from app.models.domain import Course, Domain
from app.models.scenario import ScenarioCategory


def get_all_active(session: Session) -> list[Domain]:
    return list(session.exec(
        select(Domain).where(Domain.is_active == True).order_by(Domain.order_index)
    ).all())


def get_by_slug(session: Session, slug: str) -> Optional[Domain]:
    return session.exec(select(Domain).where(Domain.slug == slug)).first()


def get_courses_by_domain(session: Session, domain_id: uuid.UUID) -> list[Course]:
    return list(session.exec(
        select(Course).where(Course.domain_id == domain_id, Course.is_active == True).order_by(Course.order_index)
    ).all())


def get_course_by_slug(session: Session, slug: str) -> Optional[Course]:
    return session.exec(select(Course).where(Course.slug == slug)).first()


def get_categories_by_course_ids(session: Session, course_ids: list[uuid.UUID]) -> list[ScenarioCategory]:
    if not course_ids:
        return []
    return list(session.exec(
        select(ScenarioCategory)
        .where(ScenarioCategory.course_id.in_(course_ids))
        .order_by(ScenarioCategory.order_index)
    ).all())
