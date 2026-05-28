# English for IT Developers - Project Rules

## Project Overview

This project is an AI-powered English learning platform for software developers.

The application helps IT developers practice English in real-world technical situations such as:
- Daily standups
- Client meetings
- Explaining bugs
- Explaining technical solutions
- Python interviews
- AWS/System Design discussions
- Code review communication

---

# Tech Stack

## Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui

## Backend
- FastAPI
- PostgreSQL
- SQLAlchemy or SQLModel
- Alembic
- JWT Authentication
- OpenAI API

---

# Architecture Rules

- Keep frontend and backend separated.
- Use service-layer architecture.
- Avoid business logic inside controllers/routes.
- Keep functions small and reusable.
- Follow clean code principles.
- Use TypeScript types everywhere in frontend.
- Use Pydantic schemas in backend.
- Use environment variables for secrets.
- Never hardcode API keys or passwords.

---

# Backend Rules

## API Structure

Use this structure:

backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── utils/
│   └── main.py

---

## Backend Standards

- Use FastAPI routers.
- Use dependency injection.
- Use JWT authentication.
- Hash passwords securely.
- Validate requests using Pydantic.
- Handle all errors gracefully.
- Use async endpoints where appropriate.
- Keep OpenAI integration inside service layer.
- Return structured JSON responses.

---

# Frontend Rules

## Frontend Structure

frontend/
├── app/
├── components/
├── services/
├── hooks/
├── lib/
├── types/
├── utils/

---

## Frontend Standards

- Use Next.js App Router.
- Use TypeScript only.
- Use Tailwind CSS.
- Use shadcn/ui components.
- Create reusable UI components.
- Handle loading and error states.
- Use responsive design.
- Avoid duplicated code.
- Keep pages clean and minimal.

---

# AI Rules

The AI feedback must include:
- corrected_version
- natural_version
- grammar_feedback
- communication_feedback
- vocabulary_suggestions
- score
- improvement_advice

The AI response format must always be valid JSON.

Focus on:
- natural English
- professional IT communication
- practical workplace English

Avoid:
- overly academic corrections
- long unnecessary explanations

---

# Product Rules

This is an MVP product.

Prioritize:
1. Simplicity
2. Clean UX
3. Fast implementation
4. Scalable architecture

Do not over-engineer the system.

Voice and realtime conversation features can be added later.

---

# Security Rules

- Never expose OpenAI API key to frontend.
- Never store plain-text passwords.
- Protect private user data.
- Validate JWT tokens for protected APIs.
- Validate ownership before returning user history.

---

# Coding Style

- Write readable code.
- Use meaningful variable names.
- Keep functions short.
- Avoid huge files.
- Use comments only when necessary.
- Prefer simple solutions over complex abstractions.


# Development Workflow

When implementing features:
1. Explain the approach first.
2. Create/update files step by step.
3. Show changed files.
4. Keep code production-ready but simple.
5. Add README instructions when needed.

---

# UI Design Direction

Style:
- modern
- clean
- developer-focused
- dark-mode friendly
- minimal but professional

Use:
- cards
- badges
- clean typography
- simple dashboards

Avoid:
- overly colorful UI
- complicated animations
- cluttered layouts

---

# Future Features

Planned future features:
- AI voice conversation
- Pronunciation scoring
- Real-time speaking practice
- Personalized learning paths
- RAG-based memory
- Interview simulation
- AI speaking coach