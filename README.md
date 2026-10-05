# AI Hackathon Idea Validator

Phase-1 production-oriented implementation based on the supplied PRD v2.0.

## Stack
- Frontend: React + TypeScript + Vite + Tailwind
- Backend: FastAPI + Pydantic + SQLAlchemy async
- Database: PostgreSQL 16
- AI: OpenAI-compatible server-side LLM adapter
- Auth: JWT + Argon2

## Run
1. Copy `.env.example` to `.env` and set `SECRET_KEY` and `LLM_API_KEY`.
2. `docker compose up --build`
3. Open http://localhost:5173
4. API docs: http://localhost:8000/docs

Without an LLM key the API uses a conservative fallback so the application can still be demonstrated locally.
