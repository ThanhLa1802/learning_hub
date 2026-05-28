import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class QuizQuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    question: str
    options: list[str]
    order_index: int
    # correct_answer_index intentionally omitted — revealed only after submission


class QuizResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lesson_id: Optional[uuid.UUID]
    title: str
    description: str
    questions: list[QuizQuestionResponse] = []


class QuizAttemptRequest(BaseModel):
    answers: list[int]


class QuizQuestionResult(BaseModel):
    question_id: uuid.UUID
    is_correct: bool
    correct_answer_index: int
    explanation: str
    your_answer_index: int


class QuizAttemptResponse(BaseModel):
    score: float
    results: list[QuizQuestionResult]
    feedback: str
