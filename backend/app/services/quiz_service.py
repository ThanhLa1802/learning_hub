from app.models.quiz import QuizQuestion


def score_attempt(questions: list[QuizQuestion], user_answers: list[int]) -> tuple[float, list[dict]]:
    """Score a quiz attempt. Returns (score_percentage, per_question_results)."""
    if not questions:
        return 0.0, []

    results = []
    correct_count = 0

    for i, question in enumerate(questions):
        user_answer = user_answers[i] if i < len(user_answers) else -1
        is_correct = user_answer == question.correct_answer_index
        if is_correct:
            correct_count += 1
        results.append({
            "question_id": question.id,
            "is_correct": is_correct,
            "correct_answer_index": question.correct_answer_index,
            "explanation": question.explanation,
            "your_answer_index": user_answer,
        })

    score = round((correct_count / len(questions)) * 100, 1)
    return score, results


def get_score_feedback(score: float) -> str:
    if score >= 90:
        return "Excellent! You have a strong grasp of this topic."
    elif score >= 70:
        return "Good work! Review the questions you missed to solidify your understanding."
    elif score >= 50:
        return "Decent effort. Study the explanations for incorrect answers and try again."
    else:
        return "This topic needs more study. Read the lesson again and retry the quiz."
