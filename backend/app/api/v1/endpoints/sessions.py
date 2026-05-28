import json
import uuid

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.api.v1.deps import CurrentUser, SessionDep
from app.repositories import progress as progress_crud
from app.repositories import scenario as scenario_crud
from app.repositories import session as session_crud
from app.models.domain import Course
from app.models.scenario import PracticeMode
from app.models.session import MessageRole, SessionStatus
from app.schemas.scenario import ScenarioCategoryResponse, ScenarioResponse
from app.schemas.session import (
    AddMessageRequest,
    CompleteSessionRequest,
    CreateSessionRequest,
    PaginatedSessionsResponse,
    PracticeSessionResponse,
    SessionMessageResponse,
)
from app.services import ai_service

router = APIRouter()


def _build_session_response(db_session, practice_session) -> PracticeSessionResponse:
    scenario = scenario_crud.get_by_id(db_session, practice_session.scenario_id)
    category = scenario_crud.get_category_by_id(db_session, scenario.category_id) if scenario else None
    messages = session_crud.get_messages(db_session, practice_session.id)

    scenario_resp = None
    if scenario:
        scenario_resp = ScenarioResponse.model_validate(scenario)
        scenario_resp.category = ScenarioCategoryResponse.model_validate(category) if category else None

    return PracticeSessionResponse(
        **practice_session.model_dump(),
        scenario=scenario_resp,
        messages=[SessionMessageResponse.model_validate(m) for m in messages],
    )


@router.post("/", response_model=PracticeSessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(request: CreateSessionRequest, session: SessionDep, current_user: CurrentUser):
    scenario = scenario_crud.get_by_id(session, request.scenario_id)
    if not scenario or not scenario.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")

    practice_session = session_crud.create(session, current_user.id, scenario.id, scenario.mode)
    return _build_session_response(session, practice_session)


@router.get("/", response_model=PaginatedSessionsResponse)
def list_sessions(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 10):
    limit = min(limit, 50)
    items, total = session_crud.get_user_sessions(session, current_user.id, skip=skip, limit=limit)
    response_items = [_build_session_response(session, ps) for ps in items]
    return PaginatedSessionsResponse(items=response_items, total=total, skip=skip, limit=limit)


@router.get("/{session_id}", response_model=PracticeSessionResponse)
def get_session(session_id: uuid.UUID, session: SessionDep, current_user: CurrentUser):
    practice_session = session_crud.get_by_id(session, session_id)
    if not practice_session or practice_session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return _build_session_response(session, practice_session)


@router.post("/{session_id}/messages", response_model=list[SessionMessageResponse])
def add_message(session_id: uuid.UUID, request: AddMessageRequest, session: SessionDep, current_user: CurrentUser):
    practice_session = session_crud.get_by_id(session, session_id)
    if not practice_session or practice_session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    if practice_session.status == SessionStatus.completed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session already completed")
    if practice_session.mode != PracticeMode.ai_chat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Messages only available for ai_chat mode")

    user_msg = session_crud.add_message(session, session_id, MessageRole.user, request.content)

    scenario = scenario_crud.get_by_id(session, practice_session.scenario_id)
    existing_messages = session_crud.get_messages(session, session_id)
    history = [{"role": m.role.value, "content": m.content} for m in existing_messages]
    ai_reply = ai_service.chat_turn(scenario, history)

    ai_msg = session_crud.add_message(session, session_id, MessageRole.assistant, ai_reply)
    return [SessionMessageResponse.model_validate(user_msg), SessionMessageResponse.model_validate(ai_msg)]


@router.post("/{session_id}/messages/stream")
def add_message_stream(session_id: uuid.UUID, request: AddMessageRequest, session: SessionDep, current_user: CurrentUser):
    practice_session = session_crud.get_by_id(session, session_id)
    if not practice_session or practice_session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    if practice_session.status == SessionStatus.completed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session already completed")
    if practice_session.mode != PracticeMode.ai_chat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Messages only available for ai_chat mode")

    user_msg = session_crud.add_message(session, session_id, MessageRole.user, request.content)
    scenario = scenario_crud.get_by_id(session, practice_session.scenario_id)
    existing_messages = session_crud.get_messages(session, session_id)
    history = [{"role": m.role.value, "content": m.content} for m in existing_messages]

    def generate():
        yield f"data: {json.dumps({'type': 'user_msg', 'id': str(user_msg.id), 'content': user_msg.content})}\n\n"
        full_content = ""
        for token in ai_service.chat_turn_stream(scenario, history):
            full_content += token
            yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
        ai_msg = session_crud.add_message(session, session_id, MessageRole.assistant, full_content)
        yield f"data: {json.dumps({'type': 'done', 'id': str(ai_msg.id)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/{session_id}/complete", response_model=PracticeSessionResponse)
def complete_session(session_id: uuid.UUID, request: CompleteSessionRequest, session: SessionDep, current_user: CurrentUser):
    practice_session = session_crud.get_by_id(session, session_id)
    if not practice_session or practice_session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    if practice_session.status == SessionStatus.completed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session already completed")

    scenario = scenario_crud.get_by_id(session, practice_session.scenario_id)

    if practice_session.mode == PracticeMode.text_response:
        if not request.user_response:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_response required for text_response mode")
        session_crud.add_message(session, session_id, MessageRole.user, request.user_response)
        feedback = ai_service.evaluate_response(scenario, request.user_response, request.lang)
    else:
        messages = session_crud.get_messages(session, session_id)
        if not messages:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No messages to evaluate")
        history = [{"role": m.role.value, "content": m.content} for m in messages]
        feedback = ai_service.evaluate_conversation(scenario, history, request.lang)

    overall_score = feedback.get("overall_score", 0)
    completed = session_crud.complete(session, practice_session, overall_score, feedback)

    # Update domain progress if the scenario belongs to a domain
    category = scenario_crud.get_category_by_id(session, scenario.category_id) if scenario else None
    if category and category.course_id:
        course = session.get(Course, category.course_id)
        if course:
            progress_crud.increment_sessions(session, current_user.id, course.domain_id)

    return _build_session_response(session, completed)
