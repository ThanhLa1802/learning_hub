---
name: add-learn-content
description: 'Add new learning content: domains, courses, lessons, quizzes, or practice scenarios to the seed files. Use when creating new topics, tech domains, learning modules, or practice scenarios for the platform.'
argument-hint: 'Mô tả nội dung cần thêm (e.g. "thêm domain Vue.js" hoặc "thêm scenario về code review")'
---

# Add Learning Content

## Cấu trúc dữ liệu học tập

```
Domain (e.g. "Python Development")
  └── Course (e.g. "Python Fundamentals")
        ├── Lesson (content + optional quiz)
        └── Quiz (questions + answers)

ScenarioCategory (linked to Course)
  └── Scenario (practice roleplay/text)
```

## 1. Thêm Domain mới

Tạo file mới: `backend/app/db/seed_<domain_slug>.py`

```python
DOMAIN = {
    "slug": "vue-js",              # unique, lowercase, hyphens
    "name": "Vue.js Development",
    "description": "...",
    "icon_name": "triangle",       # lucide icon name
    "color": "green",              # tailwind color name
    "order_index": 4,              # thứ tự hiển thị
    "is_active": True,
}

COURSE = {
    "slug": "vue-js-fundamentals",
    "name": "Vue.js Fundamentals",
    "description": "...",
    "order_index": 1,
    "is_active": True,
}
```

Đăng ký trong `backend/app/main.py` — thêm vào danh sách seed functions được gọi lúc startup.

## 2. Thêm Lesson + Quiz (TOPICS pattern)

Mỗi topic là một dict chứa `lesson` và `quiz`:

```python
TOPICS = [
    {
        "name": "topic_slug",        # dùng làm category name
        "title": "Topic Title",
        "description": "...",
        "icon_name": "code",
        "order_index": 1,
        "lesson": {
            "title": "Lesson Title",
            "content": """# Markdown content

Lesson content viết bằng Markdown.
Code blocks dùng triple backtick với language.
""",
            "content_type": LessonContentType.article,  # article | video | interactive
            "estimated_minutes": 10,
            "order_index": 1,
        },
        "quiz": {                     # Bỏ qua nếu không cần quiz
            "title": "Quiz Title",
            "passing_score": 80,
            "questions": [
                {
                    "text": "Câu hỏi?",
                    "options": ["A", "B", "C", "D"],
                    "correct_index": 0,
                    "explanation": "Giải thích tại sao A đúng.",
                },
            ],
        },
    },
]
```

## 3. Thêm Practice Scenarios

```python
SCENARIOS = [
    {
        "category": "category_slug",  # phải khớp với tên category đã có
        "title": "Scenario Title",
        "description": "Mô tả situation và task cho user (2-4 câu).",
        "mode": PracticeMode.text_response,   # text_response | roleplay
        "difficulty": Difficulty.beginner,    # beginner | intermediate | advanced
        "tags": ["tag1", "tag2"],
        "order_index": 1,
        "system_prompt": "",  # Để trống cho text_response; điền cho roleplay
    },
]
```

**Roleplay system_prompt mẫu:**
```
You are a senior developer conducting a code review. The user has submitted a PR.
Ask about their implementation choices. Be constructive but challenging.
Respond in 2-3 sentences per turn.
```

## 4. Thêm bản dịch Tiếng Việt

File: `backend/app/db/translations_vi.py`

```python
DOMAIN_TRANSLATIONS = {
    "vue-js": {
        "name": "Lập trình Vue.js",
        "description": "...",
    },
}
LESSON_TRANSLATIONS = {
    "lesson-slug": {
        "title": "Tiêu đề bài học",
        "content": "# Nội dung tiếng Việt...",
    },
}
```

## Checklist

- [ ] `slug` là unique, lowercase, dùng hyphens
- [ ] `order_index` không trùng với items cùng level
- [ ] Quiz `correct_index` là 0-based index trong mảng `options`
- [ ] `passing_score` để 80 (theo convention của project)
- [ ] Scenario `system_prompt` điền đầy đủ nếu `mode = roleplay`
- [ ] Seed function được gọi trong `backend/app/main.py`
- [ ] Thêm bản dịch VI vào `translations_vi.py` nếu cần

## Tham khảo

Xem file seed có sẵn để nắm pattern:
- [seed_react.py](../../backend/app/db/seed_react.py) — pattern đầy đủ nhất
- [seed_go.py](../../backend/app/db/seed_go.py) — domain thứ 2
- [translations_vi.py](../../backend/app/db/translations_vi.py) — bản dịch VI
