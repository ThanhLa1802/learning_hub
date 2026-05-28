import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Session, func, select

from app.models.scenario import PracticeMode
from app.models.session import MessageRole, PracticeSession, SessionMessage, SessionStatus


def create(session: Session, user_id: uuid.UUID, scenario_id: uuid.UUID, mode: PracticeMode) -> PracticeSession:
    practice_session = PracticeSession(user_id=user_id, scenario_id=scenario_id, mode=mode)
    session.add(practice_session)
    session.commit()
    session.refresh(practice_session)
    return practice_session


def get_by_id(session: Session, session_id: uuid.UUID) -> Optional[PracticeSession]:
    return session.get(PracticeSession, session_id)


def get_user_sessions(session: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 10):
    query = select(PracticeSession).where(PracticeSession.user_id == user_id)
    total = session.exec(select(func.count()).select_from(query.subquery())).one()
    items = list(session.exec(query.order_by(PracticeSession.started_at.desc()).offset(skip).limit(limit)).all())
    return items, total


def get_messages(session: Session, session_id: uuid.UUID) -> list[SessionMessage]:
    return list(
        session.exec(select(SessionMessage).where(SessionMessage.session_id == session_id).order_by(SessionMessage.created_at)).all()
    )


def add_message(session: Session, session_id: uuid.UUID, role: MessageRole, content: str) -> SessionMessage:
    msg = SessionMessage(session_id=session_id, role=role, content=content)
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg


def complete(session: Session, practice_session: PracticeSession, overall_score: int, ai_feedback: dict) -> PracticeSession:
    practice_session.status = SessionStatus.completed
    practice_session.completed_at = datetime.now(timezone.utc)
    practice_session.overall_score = overall_score
    practice_session.ai_feedback = ai_feedback
    session.add(practice_session)
    session.commit()
    session.refresh(practice_session)
    return practice_session
