import json

from openai import OpenAI

from app.core.config import settings
from app.models.scenario import Scenario

client = OpenAI(api_key=settings.openai_api_key)

EVALUATION_SYSTEM_PROMPT = """You are an expert English language coach specializing in IT and software development communication.

Your task is to evaluate a developer's English response to an IT workplace scenario.

Return ONLY valid JSON matching this exact schema (no extra text):
{{
    "overall_score": <integer 0-100>,
    "grammar_score": <integer 0-100>,
    "vocabulary_score": <integer 0-100>,
    "professionalism_score": <integer 0-100>,
    "it_appropriateness_score": <integer 0-100>,
    "strengths": ["<strength 1>", "<strength 2>"],
    "improvements": ["<improvement 1>", "<improvement 2>"],
    "corrected_example": "<a corrected or improved version of their response>",
    "natural_version": "<a native-speaker natural version for this scenario>"
}}

Focus on:
- Practical, workplace-appropriate English
- Professional IT communication norms
- Clarity and conciseness
- Technical vocabulary usage
Be constructive and encouraging. Keep feedback actionable.
Language instruction: {{lang_instruction}}"""


def evaluate_response(scenario: Scenario, user_response: str, lang: str = "en") -> dict:
    lang_instruction = "Write ALL feedback text in Vietnamese (Tiếng Việt). Keep corrected_example and natural_version in English." if lang == "vi" else "Respond in English."
    system_prompt = EVALUATION_SYSTEM_PROMPT.format(lang_instruction=lang_instruction)
    user_message = f"""Scenario: {scenario.title}
Context: {scenario.description}

Developer's response:
{user_response}"""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    return json.loads(response.choices[0].message.content)


def chat_turn(scenario: Scenario, messages: list[dict]) -> str:
    full_messages = [{"role": "system", "content": scenario.system_prompt}] + messages
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=full_messages,
        temperature=0.7,
    )
    return response.choices[0].message.content


def chat_turn_stream(scenario: Scenario, messages: list[dict]):
    full_messages = [{"role": "system", "content": scenario.system_prompt}] + messages
    stream = client.chat.completions.create(
        model=settings.openai_model,
        messages=full_messages,
        temperature=0.7,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            yield delta.content


def evaluate_conversation(scenario: Scenario, messages: list[dict], lang: str = "en") -> dict:
    transcript = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
    lang_instruction = "Write ALL feedback text in Vietnamese (Tiếng Việt). Keep corrected_example and natural_version in English." if lang == "vi" else "Respond in English."
    system_prompt = EVALUATION_SYSTEM_PROMPT.format(lang_instruction=lang_instruction)
    user_message = f"""Scenario: {scenario.title}
Context: {scenario.description}
Mode: AI roleplay conversation evaluation

Full conversation transcript:
{transcript}

Evaluate the USER's overall English communication performance throughout this conversation."""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    return json.loads(response.choices[0].message.content)
