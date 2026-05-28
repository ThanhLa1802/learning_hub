import uuid
from datetime import datetime

from sqlmodel import Session, select

from app.models.domain import Domain
from app.models.progress import UserDomainProgress


def get_or_create(session: Session, user_id: uuid.UUID, domain_id: uuid.UUID) -> UserDomainProgress:
    existing = session.exec(
        select(UserDomainProgress)
        .where(UserDomainProgress.user_id == user_id, UserDomainProgress.domain_id == domain_id)
    ).first()
    if existing:
        return existing
    progress = UserDomainProgress(user_id=user_id, domain_id=domain_id)
    session.add(progress)
    session.commit()
    session.refresh(progress)
    return progress


def get_all_for_user(session: Session, user_id: uuid.UUID) -> list[tuple[UserDomainProgress, Domain]]:
    domains = session.exec(select(Domain).where(Domain.is_active == True).order_by(Domain.order_index)).all()
    result = []
    for domain in domains:
        progress = get_or_create(session, user_id, domain.id)
        result.append((progress, domain))
    return result


def increment_sessions(session: Session, user_id: uuid.UUID, domain_id: uuid.UUID) -> None:
    progress = get_or_create(session, user_id, domain_id)
    progress.sessions_completed += 1
    progress.last_activity_at = datetime.utcnow()
    session.add(progress)
    session.commit()


def increment_lessons(session: Session, user_id: uuid.UUID, domain_id: uuid.UUID) -> None:
    progress = get_or_create(session, user_id, domain_id)
    progress.lessons_completed += 1
    progress.last_activity_at = datetime.utcnow()
    session.add(progress)
    session.commit()


def update_quiz_score(session: Session, user_id: uuid.UUID, domain_id: uuid.UUID, score: float) -> None:
    progress = get_or_create(session, user_id, domain_id)
    total = progress.avg_quiz_score * progress.quizzes_taken + score
    progress.quizzes_taken += 1
    progress.avg_quiz_score = round(total / progress.quizzes_taken, 1)
    progress.last_activity_at = datetime.utcnow()
    session.add(progress)
    session.commit()
