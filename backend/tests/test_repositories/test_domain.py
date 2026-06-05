import uuid
import pytest
from sqlmodel import Session

from app.repositories import domain as domain_crud
from app.models.domain import Domain, Course
from app.models.scenario import ScenarioCategory


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_domain(session: Session, slug: str = "python", order_index: int = 0, is_active: bool = True) -> Domain:
    domain = Domain(
        slug=slug,
        name=f"Domain {slug}",
        description="desc",
        icon_name="code",
        color="blue",
        order_index=order_index,
        is_active=is_active,
    )
    session.add(domain)
    session.commit()
    session.refresh(domain)
    return domain


def make_course(session: Session, domain: Domain, slug: str = "c1", order_index: int = 0, is_active: bool = True) -> Course:
    course = Course(
        domain_id=domain.id,
        slug=slug,
        name=f"Course {slug}",
        description="desc",
        order_index=order_index,
        is_active=is_active,
    )
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


def make_category(session: Session, course: Course, name: str = "cat1", order_index: int = 0) -> ScenarioCategory:
    cat = ScenarioCategory(
        course_id=course.id,
        name=name,
        title=f"Category {name}",
        description="desc",
        icon_name="tag",
        order_index=order_index,
    )
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


# ── get_all_active ─────────────────────────────────────────────────────────────

def test_get_all_active_returns_only_active(session: Session):
    make_domain(session, slug="active-domain", is_active=True)
    make_domain(session, slug="inactive-domain", is_active=False)

    results = domain_crud.get_all_active(session)

    assert len(results) == 1
    assert results[0].slug == "active-domain"


def test_get_all_active_returns_empty_when_none(session: Session):
    results = domain_crud.get_all_active(session)
    assert results == []


def test_get_all_active_ordered_by_order_index(session: Session):
    make_domain(session, slug="second", order_index=2)
    make_domain(session, slug="first", order_index=1)
    make_domain(session, slug="third", order_index=3)

    results = domain_crud.get_all_active(session)

    assert [r.slug for r in results] == ["first", "second", "third"]


# ── get_by_slug ────────────────────────────────────────────────────────────────

def test_get_by_slug_returns_domain(session: Session):
    make_domain(session, slug="python")

    result = domain_crud.get_by_slug(session, "python")

    assert result is not None
    assert result.slug == "python"


def test_get_by_slug_returns_none_for_unknown(session: Session):
    result = domain_crud.get_by_slug(session, "nonexistent")
    assert result is None


def test_get_by_slug_is_exact_match(session: Session):
    make_domain(session, slug="python")

    result = domain_crud.get_by_slug(session, "pytho")

    assert result is None


# ── get_courses_by_domain ──────────────────────────────────────────────────────

def test_get_courses_by_domain_returns_active_only(session: Session):
    domain = make_domain(session)
    make_course(session, domain, slug="active", is_active=True)
    make_course(session, domain, slug="inactive", is_active=False)

    results = domain_crud.get_courses_by_domain(session, domain.id)

    assert len(results) == 1
    assert results[0].slug == "active"


def test_get_courses_by_domain_returns_empty_for_unknown_domain(session: Session):
    results = domain_crud.get_courses_by_domain(session, uuid.uuid4())
    assert results == []


def test_get_courses_by_domain_ordered_by_order_index(session: Session):
    domain = make_domain(session)
    make_course(session, domain, slug="c2", order_index=2)
    make_course(session, domain, slug="c1", order_index=1)

    results = domain_crud.get_courses_by_domain(session, domain.id)

    assert [r.slug for r in results] == ["c1", "c2"]


def test_get_courses_by_domain_does_not_return_other_domain_courses(session: Session):
    d1 = make_domain(session, slug="d1")
    d2 = make_domain(session, slug="d2")
    make_course(session, d1, slug="d1-course")
    make_course(session, d2, slug="d2-course")

    results = domain_crud.get_courses_by_domain(session, d1.id)

    assert len(results) == 1
    assert results[0].slug == "d1-course"


# ── get_course_by_slug ─────────────────────────────────────────────────────────

def test_get_course_by_slug_returns_course(session: Session):
    domain = make_domain(session)
    make_course(session, domain, slug="fundamentals")

    result = domain_crud.get_course_by_slug(session, "fundamentals")

    assert result is not None
    assert result.slug == "fundamentals"


def test_get_course_by_slug_returns_none_for_unknown(session: Session):
    result = domain_crud.get_course_by_slug(session, "nonexistent")
    assert result is None


# ── get_categories_by_course_ids ───────────────────────────────────────────────

def test_get_categories_by_course_ids_returns_matching(session: Session):
    domain = make_domain(session)
    course = make_course(session, domain)
    make_category(session, course, name="cat1")
    make_category(session, course, name="cat2")

    results = domain_crud.get_categories_by_course_ids(session, [course.id])

    assert len(results) == 2
    assert {c.name for c in results} == {"cat1", "cat2"}


def test_get_categories_by_course_ids_returns_empty_for_empty_list(session: Session):
    results = domain_crud.get_categories_by_course_ids(session, [])
    assert results == []


def test_get_categories_by_course_ids_returns_empty_for_unknown_ids(session: Session):
    results = domain_crud.get_categories_by_course_ids(session, [uuid.uuid4()])
    assert results == []


def test_get_categories_by_course_ids_filters_by_course(session: Session):
    domain = make_domain(session)
    c1 = make_course(session, domain, slug="c1")
    c2 = make_course(session, domain, slug="c2")
    make_category(session, c1, name="c1-cat")
    make_category(session, c2, name="c2-cat")

    results = domain_crud.get_categories_by_course_ids(session, [c1.id])

    assert len(results) == 1
    assert results[0].name == "c1-cat"


def test_get_categories_by_course_ids_spans_multiple_courses(session: Session):
    domain = make_domain(session)
    c1 = make_course(session, domain, slug="c1")
    c2 = make_course(session, domain, slug="c2")
    make_category(session, c1, name="c1-cat")
    make_category(session, c2, name="c2-cat")

    results = domain_crud.get_categories_by_course_ids(session, [c1.id, c2.id])

    assert len(results) == 2


def test_get_categories_ordered_by_order_index(session: Session):
    domain = make_domain(session)
    course = make_course(session, domain)
    make_category(session, course, name="b-cat", order_index=2)
    make_category(session, course, name="a-cat", order_index=1)

    results = domain_crud.get_categories_by_course_ids(session, [course.id])

    assert [r.name for r in results] == ["a-cat", "b-cat"]
