# English for IT Developers

## Build, lint, and run commands

### Root

- Start the full stack with Docker: `docker compose up --build`

### Frontend (`frontend`)

- Install deps: `npm install`
- Dev server: `npm run dev`
- Production build: `npm run build`
- Lint the app: `npm run lint`
- Lint a single file: `npx eslint src/app/(main)/practice/[sessionId]/page.tsx`

### Backend (`backend`)

- Install deps: `pip install -r requirements.txt`
- Run API locally: `uvicorn app.main:app --reload --port 8000`

### Tests

- There is currently no automated test suite or test runner configured in this repository. Do not invent `pytest`, `jest`, or `npm test` commands unless a real test setup is added first.

## High-level architecture

- This repo has two user-facing product flows backed by the same FastAPI API:
  - **Practice flow**: scenario catalog, practice sessions, AI roleplay chat, and AI-written feedback
  - **Learning flow**: domains, courses, lessons, quizzes, and per-domain progress tracking
- The frontend is a Next.js App Router app under `frontend/src/app`:
  - `src/app/(main)` is the authenticated learner experience
  - `src/app/admin` is a separate admin surface with its own layout and admin check
  - `src/app/layout.tsx` mounts `AuthProvider`; `src/app/(main)/layout.tsx` adds `LangProvider` and the shared navbar
- The backend API is mounted under `/api/v1` and is split by product area:
  - `/auth`, `/users` for cookie-based auth and current-user lookup
  - `/scenarios`, `/sessions` for practice mode
  - `/domains`, `/lessons`, `/quizzes`, `/progress` for structured learning
  - `/admin` for content management of domains, courses, and lessons
- FastAPI startup (`backend/app/main.py`) does more than boot the app:
  - creates SQLModel tables
  - applies an idempotent schema tweak for `scenario_categories.course_id`
  - seeds initial domains, courses, lessons, quizzes, and scenarios on startup
- Persistence is centered on SQLModel models with PostgreSQL JSONB fields:
  - `Domain -> Course -> Lesson/Quiz`
  - `ScenarioCategory` is also linked to `Course`, which lets practice topics and learning content share the same taxonomy
  - user progress is aggregated in `UserDomainProgress` and updated from lesson completion, quiz submission, and session completion paths
- OpenAI usage is intentionally isolated in the service layer:
  - `lesson_service.py` handles AI lesson explanations
  - `ai_service.py` handles practice scoring, chat turns, and streaming chat tokens
  - routes orchestrate repositories and services; they should stay thin

## Backend conventions

- **Repository imports use the `_crud` alias**: `from app.repositories import lesson as lesson_crud`. Never import the module name bare.
- **Repositories are module-level functions**, not classes. First param is `Session`, never `SessionDep`. No `HTTPException`, no business logic.
- **PK lookups**: `session.get(Model, id)`. Filtered queries: `session.exec(select(...).where(...)).all()`. Always wrap list results in `list(...)`.
- **Response schemas**: build with `model_validate(obj)` (not deprecated `from_orm`). Computed fields (e.g. `is_completed`) are set on the schema instance **after** `model_validate`, not in the schema definition.
- **`apply_lang`** must be called on the response schema instance, not on the raw model. It mutates in-place and returns nothing. For nested objects (e.g. courses inside a domain), loop and call `apply_lang` on each child.
- **PATCH updates**: use `body.model_dump(exclude_none=True)` to apply only provided fields.
- **Unused auth**: use `_: CurrentUser` when auth must be enforced but the user object isn't needed.
- **`__init__.py` registration**: new model, schema, and repository files must be manually added to their respective `__init__.py`. Model imports in `main.py` must be in FK-resolution order (parent before child).
- **Admin authorization is not global**: each admin endpoint file defines a local `require_admin` and `AdminDep = Depends(require_admin)`. Add it manually to every new admin route.
- **New seed files** must be registered in `main.py` lifespan. See existing `seed_react.py`, `seed_go.py` for the pattern.

## Frontend conventions

- **All feature pages must be `'use client'`** — cookie-based auth does not work in Next.js Server Components.
- **API client split**: practice/auth/admin calls → `@/lib/apiClient.ts`; learning flow calls → `@/services/learnApi.ts`. Never create a new Axios instance.
- **Admin TypeScript interfaces** (`AdminDomain`, `AdminCourse`, etc.) are defined in `@/lib/apiClient.ts`, not in `@/types/`.
- **`useLang` import**: pages under `(main)/` must import from `@/contexts/LangContext` (context-backed, synced with `LangProvider`). The standalone `@/hooks/useLang` exists but is not in sync with `LangProvider`.
- **`lang` in `useEffect` deps**: any `useEffect` that calls an API accepting `lang` must list `lang` in its dependency array so it re-fetches on language toggle.
- **Error extraction**: always read `err?.response?.data?.detail` from Axios errors, not `err.message`.
- **Forms**: use `className="input"` (global CSS utility in `globals.css`) on raw `<input>`, `<select>`, `<textarea>`. This is not a shadcn component.
- **Loading state**: use `animate-pulse` skeleton divs (e.g. `<div className="h-8 bg-muted animate-pulse rounded" />`), not a spinner.
- **Admin layout is self-contained**: it calls `usersApi.me()` directly for auth. Do not refactor it to use `useAuth()`.

## Key conventions

- **Authentication is cookie-based, not bearer-token-based.**
  - Backend auth endpoints set `access_token` and `refresh_token` as httpOnly cookies.
  - Protected endpoints resolve `CurrentUser` from cookies in `backend/app/api/v1/deps.py`.
  - Frontend API calls must use the shared Axios client with `withCredentials: true`.
- **401 refresh behavior lives in one place.**
  - `frontend/src/lib/api.ts` owns the Axios instance and refresh queue logic.
  - Feature-specific clients (`src/lib/apiClient.ts`, `src/services/learnApi.ts`) should build on that shared client instead of duplicating auth handling.
- **Bilingual content is handled through `lang` query params plus JSONB translations.**
  - Models such as domains, courses, lessons, quizzes, scenarios, and categories store localized overrides in `translations`.
  - Backend responses call `apply_lang(...)` to mutate response models in place for `lang=vi`.
  - Frontend learning and practice pages should read the current language from `LangContext` and pass it through to APIs that support localization.
- **Practice mode and learning mode are separate API shapes.**
  - Practice uses `Scenario`, `PracticeSession`, `SessionMessage`, and AI feedback objects.
  - Learning uses `DomainWithCourses`, `Lesson`, `Quiz`, and `UserProgress` types from `frontend/src/types/learn.ts`.
  - Keep those type families separate instead of forcing a shared abstraction.
- **SSE streaming is part of the practice flow contract.**
  - `POST /sessions/{id}/messages/stream` emits `data:` events with `user_msg`, `token`, and `done` payload types.
  - The practice page manually reads the stream with `fetch`, not Axios, so changes to streaming behavior must preserve that contract.
- **Lesson completion is gated by quiz success when a lesson has a quiz.**
  - `POST /lessons/{id}/complete` rejects completion until the user has a passing attempt (`>= 80%`).
  - Progress updates are side effects of lesson completion, quiz submission, and completed practice sessions; preserve those links when changing related flows.
- **Admin is intentionally direct.**
  - Admin endpoints work on the same `Domain`, `Course`, and `Lesson` models used by the learner experience.
  - Admin authorization is enforced by `require_admin`; keep that check in place for new admin routes.
- **AI responses are expected to be strict JSON objects.**
  - `lesson_service.py` and `ai_service.py` call OpenAI with `response_format={"type": "json_object"}` for explanation/evaluation flows.
  - Preserve the existing response schemas when editing prompts or response types because the frontend reads concrete fields such as `overall_score`, `strengths`, `corrected_example`, and `natural_version`.
- **This project is on Next.js 16.**
  - The repo already includes a frontend-specific instruction to read the relevant Next.js docs in `node_modules/next/dist/docs/` before relying on older framework assumptions.
