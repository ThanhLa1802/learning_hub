import uuid
from typing import Optional

from sqlmodel import Session, select

from app.models.quiz import Quiz, QuizQuestion
from app.models.progress import UserQuizAttempt


def get_by_id(session: Session, quiz_id: uuid.UUID) -> Optional[Quiz]:
    return session.get(Quiz, quiz_id)


def get_questions(session: Session, quiz_id: uuid.UUID) -> list[QuizQuestion]:
    return list(session.exec(
        select(QuizQuestion).where(QuizQuestion.quiz_id == quiz_id).order_by(QuizQuestion.order_index)
    ).all())


def get_by_lesson(session: Session, lesson_id: uuid.UUID) -> Optional[Quiz]:
    return session.exec(select(Quiz).where(Quiz.lesson_id == lesson_id)).first()


def save_attempt(
    session: Session,
    user_id: uuid.UUID,
    quiz_id: uuid.UUID,
    answers: list[int],
    score: float,
) -> UserQuizAttempt:
    attempt = UserQuizAttempt(user_id=user_id, quiz_id=quiz_id, answers=answers, score=score)
    session.add(attempt)
    session.commit()
    session.refresh(attempt)
    return attempt


def has_passing_attempt(session: Session, user_id: uuid.UUID, quiz_id: uuid.UUID, min_score: float = 80.0) -> bool:
    attempt = session.exec(
        select(UserQuizAttempt)
        .where(UserQuizAttempt.user_id == user_id, UserQuizAttempt.quiz_id == quiz_id)
        .order_by(UserQuizAttempt.score.desc())
    ).first()
    return attempt is not None and attempt.score >= min_score
