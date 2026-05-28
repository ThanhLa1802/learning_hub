import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.core.database import get_session
from app.models.user import User


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session) -> User:
    from app.core.security import get_password_hash
    user = User(email="test@example.com", hashed_password=get_password_hash("password"))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="admin_user")
def admin_user_fixture(session: Session) -> User:
    from app.core.security import get_password_hash
    user = User(email="admin@example.com", hashed_password=get_password_hash("password"), is_admin=True)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="auth_cookies")
def auth_cookies_fixture(test_user: User) -> dict:
    from app.core.security import create_access_token
    token = create_access_token({"sub": str(test_user.id), "type": "access"})
    return {"access_token": token}


@pytest.fixture(name="admin_cookies")
def admin_cookies_fixture(admin_user: User) -> dict:
    from app.core.security import create_access_token
    token = create_access_token({"sub": str(admin_user.id), "type": "access"})
    return {"access_token": token}
