import uuid
import pytest
from sqlmodel import Session

from app.repositories import lesson as lesson_crud
from app.models.domain import Domain, Course
from app.models.lesson import Lesson
from app.models.scenario import ScenarioCategory


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_course(session: Session) -> Course:
    domain = Domain(
        slug=f"d-{uuid.uuid4().hex[:6]}",
        name="Test Domain",
        description="d",
        icon_name="x",
        color="blue",
        order_index=0,
    )
    session.add(domain)
    session.commit()
    course = Course(
        domain_id=domain.id,
        slug=f"c-{uuid.uuid4().hex[:6]}",
        name="Course",
        description="d",
        order_index=0,
    )
    session.add(course)
    session.commit()
    return course


def make_category(session: Session, course: Course, order_index: int = 0) -> ScenarioCategory:
    cat = ScenarioCategory(
        course_id=course.id,
        name=f"cat-{uuid.uuid4().hex[:6]}",
        title="Category",
        description="d",
        icon_name="x",
        order_index=order_index,
    )
    session.add(cat)
    session.commit()
    return cat


def make_lesson(
    session: Session,
    course: Course,
    *,
    title: str = "Lesson",
    order_index: int = 0,
    is_active: bool = True,
    category: ScenarioCategory | None = None,
) -> Lesson:
    lesson = Lesson(
        course_id=course.id,
        category_id=category.id if category else None,
        title=title,
        content="content",
        order_index=order_index,
        is_active=is_active,
    )
    session.add(lesson)
    session.commit()
    return lesson


# ── get_by_id ─────────────────────────────────────────────────────────────────

def test_get_by_id_returns_lesson(session: Session):
    course = make_course(session)
    lesson = make_lesson(session, course, title="Hello")

    result = lesson_crud.get_by_id(session, lesson.id)

    assert result is not None
    assert result.title == "Hello"


def test_get_by_id_returns_none_for_unknown_id(session: Session):
    result = lesson_crud.get_by_id(session, uuid.uuid4())
    assert result is None


# ── get_by_course ─────────────────────────────────────────────────────────────

def test_get_by_course_returns_active_lessons_only(session: Session):
    course = make_course(session)
    make_lesson(session, course, title="Active", order_index=0, is_active=True)
    make_lesson(session, course, title="Inactive", order_index=1, is_active=False)

    results = lesson_crud.get_by_course(session, course.id)

    assert len(results) == 1
    assert results[0].title == "Active"


def test_get_by_course_returns_lessons_ordered(session: Session):
    course = make_course(session)
    make_lesson(session, course, title="Second", order_index=2)
    make_lesson(session, course, title="First", order_index=1)
    make_lesson(session, course, title="Third", order_index=3)

    results = lesson_crud.get_by_course(session, course.id)

    assert [l.title for l in results] == ["First", "Second", "Third"]


def test_get_by_course_returns_empty_for_unknown_course(session: Session):
    results = lesson_crud.get_by_course(session, uuid.uuid4())
    assert results == []


# ── get_by_category ───────────────────────────────────────────────────────────

def test_get_by_category_returns_active_only(session: Session):
    course = make_course(session)
    cat = make_category(session, course)
    make_lesson(session, course, category=cat, title="Active", order_index=0, is_active=True)
    make_lesson(session, course, category=cat, title="Inactive", order_index=1, is_active=False)

    results = lesson_crud.get_by_category(session, cat.id)

    assert len(results) == 1
    assert results[0].title == "Active"


def test_get_by_category_excludes_other_categories(session: Session):
    course = make_course(session)
    cat_a = make_category(session, course, order_index=0)
    cat_b = make_category(session, course, order_index=1)
    make_lesson(session, course, category=cat_a, title="A-lesson")
    make_lesson(session, course, category=cat_b, title="B-lesson")

    results = lesson_crud.get_by_category(session, cat_a.id)

    assert len(results) == 1
    assert results[0].title == "A-lesson"


# ── is_completed / mark_complete ──────────────────────────────────────────────

def test_is_completed_returns_false_before_completion(session: Session):
    course = make_course(session)
    lesson = make_lesson(session, course)
    user_id = uuid.uuid4()

    assert lesson_crud.is_completed(session, user_id, lesson.id) is False


def test_is_completed_returns_true_after_mark_complete(session: Session):
    course = make_course(session)
    lesson = make_lesson(session, course)
    user_id = uuid.uuid4()

    lesson_crud.mark_complete(session, user_id, lesson.id)

    assert lesson_crud.is_completed(session, user_id, lesson.id) is True


def test_mark_complete_is_idempotent(session: Session):
    course = make_course(session)
    lesson = make_lesson(session, course)
    user_id = uuid.uuid4()

    p1 = lesson_crud.mark_complete(session, user_id, lesson.id)
    p2 = lesson_crud.mark_complete(session, user_id, lesson.id)

    assert p1.id == p2.id


def test_mark_complete_is_per_user(session: Session):
    course = make_course(session)
    lesson = make_lesson(session, course)
    user_a, user_b = uuid.uuid4(), uuid.uuid4()

    lesson_crud.mark_complete(session, user_a, lesson.id)

    assert lesson_crud.is_completed(session, user_a, lesson.id) is True
    assert lesson_crud.is_completed(session, user_b, lesson.id) is False


# ── get_user_completed_ids ────────────────────────────────────────────────────

def test_get_user_completed_ids_returns_correct_set(session: Session):
    course = make_course(session)
    l1 = make_lesson(session, course, title="L1")
    l2 = make_lesson(session, course, title="L2")
    l3 = make_lesson(session, course, title="L3")
    user_id = uuid.uuid4()

    lesson_crud.mark_complete(session, user_id, l1.id)
    lesson_crud.mark_complete(session, user_id, l3.id)

    completed = lesson_crud.get_user_completed_ids(session, user_id)

    assert l1.id in completed
    assert l3.id in completed
    assert l2.id not in completed


def test_get_user_completed_ids_empty_for_new_user(session: Session):
    completed = lesson_crud.get_user_completed_ids(session, uuid.uuid4())
    assert completed == set()


# ── get_next_lesson ───────────────────────────────────────────────────────────

def test_get_next_lesson_returns_none_without_category(session: Session):
    course = make_course(session)
    lesson = make_lesson(session, course)  # no category

    assert lesson_crud.get_next_lesson(session, lesson) is None


def test_get_next_lesson_returns_next_in_same_category(session: Session):
    course = make_course(session)
    cat = make_category(session, course)
    l1 = make_lesson(session, course, category=cat, title="First", order_index=1)
    l2 = make_lesson(session, course, category=cat, title="Second", order_index=2)

    result = lesson_crud.get_next_lesson(session, l1)

    assert result is not None
    assert result.id == l2.id


def test_get_next_lesson_returns_none_at_last_in_last_category(session: Session):
    course = make_course(session)
    cat = make_category(session, course, order_index=0)
    last = make_lesson(session, course, category=cat, title="Last", order_index=99)

    result = lesson_crud.get_next_lesson(session, last)

    assert result is None


def test_get_next_lesson_crosses_to_next_category(session: Session):
    course = make_course(session)
    cat_a = make_category(session, course, order_index=1)
    cat_b = make_category(session, course, order_index=2)
    last_in_a = make_lesson(session, course, category=cat_a, title="Last-A", order_index=99)
    first_in_b = make_lesson(session, course, category=cat_b, title="First-B", order_index=1)

    result = lesson_crud.get_next_lesson(session, last_in_a)

    assert result is not None
    assert result.id == first_in_b.id
