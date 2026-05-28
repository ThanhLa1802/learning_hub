import uuid
from typing import Optional

from sqlmodel import Session, select

from app.models.lesson import Lesson
from app.models.progress import UserLessonProgress
from app.models.scenario import ScenarioCategory


def get_by_id(session: Session, lesson_id: uuid.UUID) -> Optional[Lesson]:
    return session.get(Lesson, lesson_id)


def get_by_course(session: Session, course_id: uuid.UUID) -> list[Lesson]:
    return list(session.exec(
        select(Lesson)
        .where(Lesson.course_id == course_id, Lesson.is_active == True)
        .order_by(Lesson.order_index)
    ).all())


def get_by_category(session: Session, category_id: uuid.UUID) -> list[Lesson]:
    return list(session.exec(
        select(Lesson)
        .where(Lesson.category_id == category_id, Lesson.is_active == True)
        .order_by(Lesson.order_index)
    ).all())


def get_user_completed_ids(session: Session, user_id: uuid.UUID) -> set[uuid.UUID]:
    results = session.exec(
        select(UserLessonProgress.lesson_id).where(UserLessonProgress.user_id == user_id)
    ).all()
    return set(results)


def mark_complete(session: Session, user_id: uuid.UUID, lesson_id: uuid.UUID) -> UserLessonProgress:
    existing = session.exec(
        select(UserLessonProgress)
        .where(UserLessonProgress.user_id == user_id, UserLessonProgress.lesson_id == lesson_id)
    ).first()
    if existing:
        return existing
    progress = UserLessonProgress(user_id=user_id, lesson_id=lesson_id)
    session.add(progress)
    session.commit()
    session.refresh(progress)
    return progress


def is_completed(session: Session, user_id: uuid.UUID, lesson_id: uuid.UUID) -> bool:
    return session.exec(
        select(UserLessonProgress)
        .where(UserLessonProgress.user_id == user_id, UserLessonProgress.lesson_id == lesson_id)
    ).first() is not None


def get_next_lesson(session: Session, lesson: Lesson) -> Optional[Lesson]:
    if not lesson.category_id:
        return None

    # 1. Try next lesson in the same category
    next_in_category = session.exec(
        select(Lesson)
        .where(
            Lesson.category_id == lesson.category_id,
            Lesson.is_active == True,
            Lesson.order_index > lesson.order_index,
        )
        .order_by(Lesson.order_index)
        .limit(1)
    ).first()
    if next_in_category:
        return next_in_category

    # 2. Find the next category in the same course
    current_cat = session.get(ScenarioCategory, lesson.category_id)
    if not current_cat or not current_cat.course_id:
        return None

    next_cat = session.exec(
        select(ScenarioCategory)
        .where(
            ScenarioCategory.course_id == current_cat.course_id,
            ScenarioCategory.order_index > current_cat.order_index,
        )
        .order_by(ScenarioCategory.order_index)
        .limit(1)
    ).first()
    if not next_cat:
        return None

    # 3. Return first lesson of that next category
    return session.exec(
        select(Lesson)
        .where(Lesson.category_id == next_cat.id, Lesson.is_active == True)
        .order_by(Lesson.order_index)
        .limit(1)
    ).first()
