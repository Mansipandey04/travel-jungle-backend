# Travel Jungle Backend

India-only travel experience API for **Travel Jungle** (“Find the Hidden. Feel the Story.”).

This repository **is** the FastAPI application (repo root = app root). The companion UI lives in [`travel-jungle-frontend`](https://github.com/Mansipandey04/travel-jungle-frontend).

## Stack

- FastAPI + Pydantic v2 + SQLAlchemy 2.x + Alembic + PostgreSQL
- Modular layout: `models` → `schemas` → `repositories` → `services` → `api/v1`
- Local upload volume via `StorageBackend` (S3 later)
- Admin auth: static `ADMIN_API_TOKEN` bearer (MVP)
- Community stories start as `pending`; public POSTs are rate-limited

## Sibling compose layout

Clone both repos as siblings, then run compose **from this backend repo**:

```text
travel_jungle/
  backend/     ← docker-compose.yml lives here; builds backend from `.`
  frontend/    ← default FRONTEND_CONTEXT=../frontend
```

Override if needed (e.g. separate clone names):

```bash
FRONTEND_CONTEXT=../travel-jungle-frontend docker compose up --build
```

Services: `frontend`, `backend`, `db` on network `travel-jungle-network`.

## Quick start (Docker)

```bash
cp .env.example .env
# edit placeholders only — never commit .env
docker compose up --build -d
```

- API: http://localhost:8000  
- OpenAPI docs: http://localhost:8000/docs  
- Health: http://localhost:8000/health  
- Frontend (when sibling present): http://localhost:3000  

### Migrate

Compose backend CMD runs migrations on start. Manually:

```bash
alembic upgrade head
```

### Seed (demo only)

Requires `SEED_DEMO=true`. Seeds 6 India destinations + Hidden India layers + demo-marked trips (verified facts only; no invented prices).

```bash
docker compose exec backend python -m app.seed.run_seed
# or locally:
SEED_DEMO=true DATABASE_URL=... python -m app.seed.run_seed
```

Idempotent: safe to run twice (no duplicate slugs).

## Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
# point DATABASE_URL at a local Postgres, then:
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Interactive docs: http://localhost:8000/docs

### Tests

```bash
pytest -v
```

Tests use in-memory SQLite (no Postgres required).

## Auth

```http
POST /api/v1/auth/login
{"token":"<ADMIN_API_TOKEN>"}

GET /api/v1/auth/me
Authorization: Bearer <ADMIN_API_TOKEN>
```

Also available: `POST /api/v1/admin/login`. All `/api/v1/admin/*` mutations require the bearer token.

## API surface (summary)

Base path `/api/v1` — see live OpenAPI at `/docs`.

| Method | Path | Auth |
|--------|------|------|
| GET | `/health` | public |
| GET | `/destinations`, `/destinations/{slug}` | public |
| GET | `/trips`, `/trips/{slug}` | public |
| GET | `/events`, `/events/{slug}` | public |
| GET | `/hidden-india`, `/hidden-india/{slug}` | public |
| GET | `/stories`, `/stories/{slug}` | public (approved) |
| POST | `/community/stories` | public + rate limit → `pending` |
| POST | `/enquiries`, `/contact` | public + rate limit |
| POST/PATCH/DELETE | `/admin/...` | admin bearer |
| POST | `/admin/upload` | admin bearer |

## Security notes

- Never commit secrets; `.env.example` has placeholders only.
- Schema changes via Alembic only — no `create_all` in production startup.
- Demo seed rows set `is_demo=true`.
- Browser traffic in production should stay on the frontend proxy; `:8000` is for local/debug.

## License

Private Travel Jungle MVP — personal project for Mansipandey04.
