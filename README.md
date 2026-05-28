# English for IT Developers

AI-powered English learning platform for software developers. Practice real workplace English — standups, client calls, Python interviews, code reviews — and get instant AI feedback with structured scores and suggestions.

---

## Features

- **Structured Learning** — domain-based courses with markdown lessons, quizzes, and progress tracking
- **AI Practice Chat** — roleplay real workplace scenarios with streaming AI responses (SSE)
- **Instant AI Feedback** — grammar, communication, vocabulary scoring after each practice session
- **Admin Panel** — full CRUD for domains, courses, and lessons with live markdown editor
- **JWT Auth** — httpOnly cookie-based authentication with refresh tokens
- **Multi-language UI** — English / Vietnamese toggle

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16 (App Router), React, TypeScript, Tailwind CSS, shadcn/ui |
| Backend | FastAPI, SQLModel, Alembic, PostgreSQL |
| AI | OpenAI API (gpt-4o-mini), Server-Sent Events streaming |
| Auth | JWT (httpOnly cookies, refresh tokens) |
| Infra | Docker, Docker Compose |

---

## Prerequisites

- Docker + Docker Compose
- An OpenAI API key

---

## Quick Start (Docker)

1. **Clone and set up environment**

```bash
cp .env.example .env
```

Edit `.env` and fill in:
```
OPENAI_API_KEY=sk-your-key-here
SECRET_KEY=your-random-32-char-secret
```

2. **Copy backend env**

```bash
cp backend/.env.example backend/.env
```

3. **Start all services**

```bash
docker compose up --build
```

4. **Access the app**

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API docs | http://localhost:8000/docs |
| Admin Panel | http://localhost:3000/admin |

> On first start, the database is seeded automatically with domains, courses, lessons, quizzes, and practice scenarios.

---

## Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with DATABASE_URL, SECRET_KEY, OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
# Create .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing key (32+ char random string) |
| `ALGORITHM` | JWT algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL (default: `30`) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token TTL (default: `7`) |
| `OPENAI_API_KEY` | OpenAI API key |
| `OPENAI_MODEL` | Model name (default: `gpt-4o-mini`) |
| `CORS_ORIGINS` | Comma-separated allowed origins |

### Frontend (`frontend/.env.local`)

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_URL` | Backend base URL (e.g. `http://localhost:8000`) |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                             │
│                    Next.js 16 (port 3000)                   │
│        App Router · TypeScript · Tailwind · shadcn/ui       │
└───────────────────────┬─────────────────────────────────────┘
                        │  HTTP / SSE (axios + fetch)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (port 8000)                 │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │  /auth   │  │  /learn  │  │ /sessions│  │  /admin   │  │
│  │  /users  │  │ /domains │  │/scenarios│  │  (CRUD)   │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────┘  │
│                        │                                    │
│               Service Layer                                 │
│     ai_service · lesson_service · quiz_service              │
│                        │                                    │
│              Repository Layer (SQLModel)                    │
└───────────────────────┬─────────────────────────────────────┘
                        │  SQLAlchemy / asyncpg
                        ▼
┌─────────────────────────────────────────────────────────────┐
│               PostgreSQL (port 5432)                        │
│  users · domains · courses · lessons · quizzes              │
│  scenarios · sessions · messages · progress                 │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   OpenAI API                                │
│         AI feedback · Roleplay chat · SSE streaming         │
└─────────────────────────────────────────────────────────────┘
```

**Key data flows:**
- **Auth**: Login → JWT access token (httpOnly cookie) + refresh token → auto-refreshed on expiry
- **AI Chat**: User message → FastAPI SSE endpoint → OpenAI `stream=True` → token chunks streamed to browser
- **AI Feedback**: Session complete → structured JSON scored by GPT (grammar, vocabulary, communication, score)
- **Admin**: Guarded by `is_admin` flag on User model → full CRUD on content without redeployment

---

## Codebase Structure

```
english_for_dev/
├── docker-compose.yml
├── .env.example
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   └── versions/           # Migration files
│   └── app/
│       ├── main.py             # FastAPI app entry point, lifespan, CORS
│       ├── api/
│       │   └── v1/
│       │       ├── deps.py     # Shared dependencies (CurrentUser, SessionDep)
│       │       ├── router.py   # Registers all sub-routers
│       │       └── endpoints/
│       │           ├── admin.py      # Admin CRUD (domains, courses, lessons)
│       │           ├── auth.py       # Register, login, logout, refresh
│       │           ├── domains.py    # Domain + course listing
│       │           ├── lessons.py    # Lesson content
│       │           ├── progress.py   # User progress per domain
│       │           ├── quizzes.py    # Quiz questions + submission
│       │           ├── scenarios.py  # Practice scenario catalog
│       │           ├── sessions.py   # Practice sessions + SSE streaming
│       │           └── users.py      # Current user profile
│       ├── core/
│       │   ├── config.py       # Settings (pydantic-settings)
│       │   ├── database.py     # SQLModel engine + session factory
│       │   └── security.py     # Password hashing, JWT encode/decode
│       ├── db/
│       │   ├── seed.py         # Master seed runner
│       │   ├── seed_go.py      # Go programming course seed data
│       │   └── ...             # Other domain seed files
│       ├── models/
│       │   ├── user.py         # User (id, email, hashed_password, is_admin)
│       │   ├── domain.py       # Domain, Course
│       │   ├── lesson.py       # Lesson (markdown content)
│       │   ├── quiz.py         # QuizQuestion, QuizOption
│       │   ├── scenario.py     # Scenario, ScenarioCategory
│       │   ├── session.py      # PracticeSession, SessionMessage
│       │   └── progress.py     # UserLessonProgress
│       ├── schemas/
│       │   ├── admin.py        # DomainCreate/Update, CourseCreate/Update, LessonCreate/Update
│       │   ├── auth.py         # LoginRequest, RegisterRequest, TokenResponse
│       │   ├── domain.py       # DomainResponse, CourseResponse
│       │   ├── lesson.py       # LessonResponse
│       │   ├── progress.py     # UserDomainProgressResponse
│       │   ├── quiz.py         # QuizQuestionResponse, QuizSubmitRequest
│       │   ├── scenario.py     # ScenarioResponse
│       │   ├── session.py      # SessionCreate, MessageResponse, FeedbackResponse
│       │   └── user.py         # UserResponse (includes is_admin)
│       ├── services/
│       │   ├── ai_service.py       # OpenAI chat, feedback, chat_turn_stream (SSE)
│       │   ├── lesson_service.py   # Lesson progress logic
│       │   └── quiz_service.py     # Quiz scoring logic
│       ├── repositories/       # DB query layer (separates SQL from endpoints)
│       └── utils/              # Helper utilities
│
└── frontend/
    ├── Dockerfile
    ├── package.json
    └── src/
        ├── app/
        │   ├── layout.tsx          # Root layout (font, theme)
        │   ├── page.tsx            # Landing page
        │   ├── globals.css         # Tailwind + custom .input component
        │   ├── (auth)/             # Login, Register pages
        │   ├── (main)/             # Authenticated app (shared Navbar layout)
        │   │   ├── dashboard/      # User dashboard
        │   │   ├── learn/          # Domain list, lessons, quizzes
        │   │   ├── practice/       # AI chat + text response sessions
        │   │   ├── history/        # Past session history
        │   │   └── scenarios/      # Scenario browser
        │   └── admin/              # Admin panel (own layout, guard)
        │       ├── layout.tsx      # Sidebar + is_admin check
        │       ├── page.tsx        # Dashboard with stats
        │       ├── domains/        # Domain list + new + edit
        │       ├── courses/        # Course list + new + edit
        │       └── lessons/        # Lesson list + new + edit (markdown editor)
        ├── components/
        │   ├── layout/
        │   │   └── Navbar.tsx      # Top nav with user dropdown + Admin Panel link
        │   ├── auth/               # Login/Register forms
        │   ├── scenarios/          # Scenario cards
        │   └── ui/                 # shadcn/ui components
        ├── hooks/
        │   └── useAuth.tsx         # Auth context: user, login, logout, register
        ├── lib/
        │   ├── api.ts              # Axios instance with interceptors + refresh
        │   └── apiClient.ts        # Typed API wrappers (authApi, usersApi, adminApi…)
        ├── services/
        │   └── learnApi.ts         # Learning domain API calls
        ├── types/
        │   ├── index.ts            # User, Scenario, Session, Message types
        │   └── learn.ts            # Domain, Course, Lesson, Progress types
        └── contexts/               # React context providers
```

---

## Database Schema (key tables)

```
users          — id, email, hashed_password, full_name, is_active, is_admin
domains        — id, slug, name, description, icon_name, color, order_index, is_active
courses        — id, domain_id, slug, name, description, order_index, is_active
lessons        — id, course_id, title, content (markdown), content_type, order_index
quizzes        — id, course_id, question, options (JSON), correct_answer, explanation
scenarios      — id, category_id, title, description, mode, difficulty, system_prompt
sessions       — id, user_id, scenario_id, status, feedback (JSON)
messages       — id, session_id, role (user|assistant), content
progress       — id, user_id, lesson_id, completed_at
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login → sets httpOnly cookies |
| POST | `/api/v1/auth/logout` | Clear cookies |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/users/me` | Current user profile |
| GET | `/api/v1/domains` | List learning domains |
| GET | `/api/v1/lessons/{id}` | Lesson content |
| GET | `/api/v1/quizzes/{course_id}` | Quiz for a course |
| GET | `/api/v1/scenarios` | Browse practice scenarios |
| POST | `/api/v1/sessions` | Start practice session |
| POST | `/api/v1/sessions/{id}/messages` | Send message (text mode) |
| POST | `/api/v1/sessions/{id}/messages/stream` | **SSE** — AI chat stream |
| POST | `/api/v1/sessions/{id}/complete` | End session + get AI feedback |
| GET | `/api/v1/progress/domains` | User progress per domain |
| GET | `/api/v1/admin/domains` | (Admin) List domains |
| POST | `/api/v1/admin/domains` | (Admin) Create domain |
| PUT | `/api/v1/admin/domains/{id}` | (Admin) Update domain |
| GET | `/api/v1/admin/courses` | (Admin) List courses |
| POST | `/api/v1/admin/courses` | (Admin) Create course |
| PUT | `/api/v1/admin/courses/{id}` | (Admin) Update course |
| GET | `/api/v1/admin/lessons` | (Admin) List lessons |
| GET | `/api/v1/admin/lessons/{id}` | (Admin) Get lesson with content |
| POST | `/api/v1/admin/lessons` | (Admin) Create lesson |
| PUT | `/api/v1/admin/lessons/{id}` | (Admin) Update lesson |

---

## AI Feedback Format

After each practice session the AI returns structured JSON:

```json
{
  "corrected_version": "...",
  "natural_version": "...",
  "grammar_feedback": "...",
  "communication_feedback": "...",
  "vocabulary_suggestions": ["...", "..."],
  "score": 82,
  "improvement_advice": "..."
}
```

---

## Admin Panel

Access at `/admin` — only visible to users with `is_admin = true`.

To promote a user to admin:

```bash
docker exec <postgres-container> psql -U postgres -d english_for_dev \
  -c "UPDATE users SET is_admin=true WHERE email='your@email.com';"
```

---

## Practice Modes

| Mode | Description |
|---|---|
| **Text Response** | Write a response to a scenario prompt; get structured AI feedback |
| **AI Chat** | Live conversation — AI plays a specific role (interviewer, client, tech lead); responses stream token by token |

---

## Learning Domains

| Domain | Description |
|---|---|
| Daily Standup | Report progress, blockers, plans in natural English |
| Client Meetings | Handle questions, explain delays, manage expectations |
| Explaining Bugs | Describe root cause and fix clearly to stakeholders |
| Python Interview | Practice common Python technical interview questions |
| AWS / System Design | Discuss cloud architecture and scalability |
| Code Review | Give and receive professional code feedback |
| Go Programming | Learn Go fundamentals through structured lessons and quizzes |
