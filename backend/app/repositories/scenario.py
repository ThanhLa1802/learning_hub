import uuid
from typing import Optional

from sqlmodel import Session, select

from app.models.scenario import Difficulty, PracticeMode, Scenario, ScenarioCategory


def get_categories(session: Session) -> list[ScenarioCategory]:
    return list(session.exec(select(ScenarioCategory).order_by(ScenarioCategory.order_index)).all())


def get_all(
    session: Session,
    category_id: Optional[uuid.UUID] = None,
    difficulty: Optional[Difficulty] = None,
    mode: Optional[PracticeMode] = None,
) -> list[Scenario]:
    query = select(Scenario).where(Scenario.is_active == True)
    if category_id:
        query = query.where(Scenario.category_id == category_id)
    if difficulty:
        query = query.where(Scenario.difficulty == difficulty)
    if mode:
        query = query.where(Scenario.mode == mode)
    return list(session.exec(query.order_by(Scenario.order_index)).all())


def get_by_id(session: Session, scenario_id: uuid.UUID) -> Optional[Scenario]:
    return session.get(Scenario, scenario_id)


def get_category_by_id(session: Session, category_id: uuid.UUID) -> Optional[ScenarioCategory]:
    return session.get(ScenarioCategory, category_id)
