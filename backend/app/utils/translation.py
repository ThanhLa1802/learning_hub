"""
Translation helper: merges translations.{lang}.* into a response dict.

Usage:
    resp = LessonResponse.model_validate(lesson)
    apply_lang(resp, lesson.translations, lang)
"""

from typing import Any


SUPPORTED_LANGS = {"en", "vi"}
DEFAULT_LANG = "en"


def apply_lang(response: Any, translations: dict | None, lang: str) -> None:
    """
    Mutate `response` in-place, overwriting translatable fields with the
    values stored in translations[lang] when lang != 'en' and translations exist.
    """
    if lang == DEFAULT_LANG or not translations:
        return
    if lang not in SUPPORTED_LANGS:
        return
    lang_data: dict = translations.get(lang, {})
    if not lang_data:
        return
    for field, value in lang_data.items():
        if hasattr(response, field):
            setattr(response, field, value)
