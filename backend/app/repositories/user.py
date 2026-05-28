import uuid
from typing import Optional

from sqlmodel import Session, select

from app.models.user import User


def get_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()


def get_by_id(session: Session, user_id: uuid.UUID) -> Optional[User]:
    return session.get(User, user_id)


def create(session: Session, email: str, hashed_password: str, full_name: str) -> User:
    user = User(email=email, hashed_password=hashed_password, full_name=full_name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
