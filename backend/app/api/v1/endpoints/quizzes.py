import uuid

from fastapi import APIRouter, HTTPException, status

from app.api.v1.deps import CurrentUser, SessionDep
from app.repositories import progress as progress_crud
from app.repositories import quiz as quiz_crud
from app.models.domain import Course
from app.schemas.quiz import (
    QuizAttemptRequest,
    QuizAttemptResponse,
    QuizQuestionResponse,
    QuizQuestionResult,
    QuizResponse,
)
from app.services import quiz_service
from app.utils.translation import apply_lang

router = APIRouter()


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: uuid.UUID, session: SessionDep, _: CurrentUser, lang: str = "en"):
    quiz = quiz_crud.get_by_id(session, quiz_id)
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    questions = quiz_crud.get_questions(session, quiz_id)
    response = QuizResponse.model_validate(quiz)
    apply_lang(response, quiz.translations, lang)
    response.questions = []
    for q in questions:
        qr = QuizQuestionResponse.model_validate(q)
        apply_lang(qr, q.translations, lang)
        response.questions.append(qr)
    return response


@router.post("/{quiz_id}/attempt", response_model=QuizAttemptResponse)
def submit_attempt(quiz_id: uuid.UUID, request: QuizAttemptRequest, session: SessionDep, current_user: CurrentUser):
    quiz = quiz_crud.get_by_id(session, quiz_id)
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

    questions = quiz_crud.get_questions(session, quiz_id)
    if len(request.answers) != len(questions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Expected {len(questions)} answers, got {len(request.answers)}",
        )

    score, results = quiz_service.score_attempt(questions, request.answers)
    quiz_crud.save_attempt(session, current_user.id, quiz_id, request.answers, score)

    course = session.get(Course, quiz.course_id)
    if course:
        progress_crud.update_quiz_score(session, current_user.id, course.domain_id, score)

    return QuizAttemptResponse(
        score=score,
        results=[QuizQuestionResult(**r) for r in results],
        feedback=quiz_service.get_score_feedback(score),
    )
