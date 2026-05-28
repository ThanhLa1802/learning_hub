import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, status

from app.api.v1.deps import CurrentUser, SessionDep
from app.repositories import scenario as scenario_crud
from app.models.scenario import Difficulty, PracticeMode
from app.schemas.scenario import ScenarioCategoryResponse, ScenarioResponse

router = APIRouter()


@router.get("/categories", response_model=list[ScenarioCategoryResponse])
def get_categories(session: SessionDep, _: CurrentUser):
    return scenario_crud.get_categories(session)


@router.get("/", response_model=list[ScenarioResponse])
def get_scenarios(
    session: SessionDep,
    _: CurrentUser,
    category_id: Optional[uuid.UUID] = None,
    difficulty: Optional[Difficulty] = None,
    mode: Optional[PracticeMode] = None,
):
    scenarios = scenario_crud.get_all(session, category_id=category_id, difficulty=difficulty, mode=mode)
    result = []
    for s in scenarios:
        category = scenario_crud.get_category_by_id(session, s.category_id)
        data = ScenarioResponse.model_validate(s)
        data.category = ScenarioCategoryResponse.model_validate(category) if category else None
        result.append(data)
    return result


@router.get("/{scenario_id}", response_model=ScenarioResponse)
def get_scenario(scenario_id: uuid.UUID, session: SessionDep, _: CurrentUser):
    scenario = scenario_crud.get_by_id(session, scenario_id)
    if not scenario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
    category = scenario_crud.get_category_by_id(session, scenario.category_id)
    data = ScenarioResponse.model_validate(scenario)
    data.category = ScenarioCategoryResponse.model_validate(category) if category else None
    return data
