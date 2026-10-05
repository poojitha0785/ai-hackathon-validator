# Architecture
Browser -> React/TypeScript -> FastAPI routers -> domain services/SQLAlchemy -> PostgreSQL.
Validation flow: form -> authorized idea version -> server-side LLM adapter -> validated JSON -> deterministic scoring engine -> evaluations table -> results UI.
Auth: browser bearer JWT -> FastAPI dependency -> user lookup -> ownership check.
The browser never receives the LLM secret. SQLAlchemy parameterizes SQL. Phase 1 uses local React state; a larger deployment can add TanStack Query.
