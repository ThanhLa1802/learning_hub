import json

from openai import OpenAI

from app.core.config import settings
from app.models.lesson import Lesson

client = OpenAI(api_key=settings.openai_api_key)

EXPLAIN_SYSTEM_PROMPT = """You are an expert software engineer and technical educator specializing in system design and distributed systems.

Your task is to explain a concept clearly and practically for a software developer preparing for system design interviews.

Return ONLY valid JSON matching this exact schema (no extra text):
{{
    "explanation": "<clear, practical explanation — 3-5 paragraphs>",
    "key_points": ["<key point 1>", "<key point 2>", "<key point 3>", "<key point 4>"],
    "real_world_example": "<concrete example: how Netflix, Amazon, Twitter, or similar companies use this>",
    "interview_tip": "<how to confidently discuss this concept in a system design interview>"
}}

Guidelines:
- Be practical, not academic. Focus on when and why, not just what.
- Use specific numbers and real product examples where possible.
- Keep the interview tip actionable and interview-ready.
- Do not include markdown formatting inside JSON string values.
- Language instruction: {lang_instruction}"""


def explain_concept(lesson: Lesson, user_question: str = "", lang: str = "en") -> dict:
    lang_instruction = "Respond in Vietnamese (Tiếng Việt)." if lang == "vi" else "Respond in English."
    system_prompt = EXPLAIN_SYSTEM_PROMPT.format(lang_instruction=lang_instruction)
    question_context = f"\n\nUser's specific question: {user_question}" if user_question.strip() else ""

    user_message = f"""Topic: {lesson.title}

Lesson content:
{lesson.content}{question_context}

Provide a deeper, practical explanation of this concept."""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        response_format={"type": "json_object"},
        temperature=0.4,
    )
    return json.loads(response.choices[0].message.content)
