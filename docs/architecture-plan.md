# Travel Jungle MVP — Architecture & Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. **Do not start Phase 2 until the Open Decisions section is approved.**

**Goal:** Ship an India-only travel experience & community platform (Travel Jungle — “Find the Hidden. Feel the Story.”) with editorial destination pages, trips, events, stories, community submissions, and the signature Hidden India Diaries feature — via a Dockerized Next.js + FastAPI + PostgreSQL monorepo.

**Architecture:** Strict frontend/backend separation under `travel-jungle/{frontend,backend}`. The browser talks only to Next.js; Next.js proxies `/api/backend/[...path]` to FastAPI at `BACKEND_INTERNAL_URL=http://backend:8000` on Docker network `travel-jungle-network`. FastAPI owns all Postgres access (SQLAlchemy 2.x + Alembic). Uploads live on a named volume; object storage is abstracted for later S3.

**Tech Stack:** Next.js (App Router), React, TypeScript, Tailwind, Lucide, React Hook Form, Zod, Node LTS · Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, PostgreSQL, Uvicorn · Docker Compose (multi-stage frontend standalone; slim non-root backend; healthchecks).

## Global Constraints

- India-only: all destinations, trips, events, and stories are India-scoped; no international travel in MVP.
- Brand palette (exact): Jungle Green `#183D2B`, Warm Sand `#F5F0E5`, Earth Coral `#E97848`, Golden Yellow `#D5B46A`, Leaf Sage `#DCE5D5`.
- Fonts: Playfair Display (headings), DM Sans (body / nav / buttons).
- Editorial / cinematic India photography; no generic agency stock look; no excessive gradients or animations.
- Browser never resolves Docker hostnames; frontend never connects to Postgres.
- Alembic only for schema changes — never `Base.metadata.create_all` in production paths.
- Seed / demo data must be marked as demo; never present invented prices, dates, testimonials, ratings, or availability as real.
- Community submissions start as `pending` until admin approval.
- Rate-limit public submission endpoints; admin auth required for mutating content.
- No payments in MVP.
- Out of scope: Redis, Kafka, Kubernetes, S3 (keep storage interface only), international travel.
- Phases are sequential gates — finish and verify a phase before starting the next.
- Monorepo root: `travel-jungle/` (recommended; confirm in Open Decisions).

---

## 1. Proposed Monorepo Folder Tree

```text
travel-jungle/
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── docs/
│   ├── architecture.md          # condensed from this plan
│   ├── api.md                   # OpenAPI-derived endpoint notes
│   └── seed-policy.md
├── frontend/                    # Next.js App Router
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── public/
│   │   └── images/              # static brand / placeholder assets
│   └── src/
│       ├── app/
│       │   ├── layout.tsx
│       │   ├── page.tsx                    # /
│       │   ├── explore-india/
│       │   │   ├── page.tsx
│       │   │   └── [slug]/page.tsx
│       │   ├── trips/
│       │   │   ├── page.tsx
│       │   │   └── [slug]/page.tsx
│       │   ├── events/page.tsx
│       │   ├── stories/page.tsx
│       │   ├── community/
│       │   │   ├── page.tsx
│       │   │   └── submit/page.tsx
│       │   ├── hidden-india/[slug]/page.tsx
│       │   ├── about/page.tsx
│       │   ├── contact/page.tsx
│       │   └── api/backend/[...path]/route.ts   # reverse proxy
│       ├── components/
│       │   ├── layout/          # Header, Footer, Shell
│       │   ├── ui/              # Button, Input, Textarea, etc. (interaction containers only)
│       │   ├── destination/
│       │   ├── trip/
│       │   ├── event/
│       │   ├── story/
│       │   ├── hidden-india/    # Discover / Experience / Explore layers
│       │   └── forms/           # Enquiry, Contact, CommunitySubmit
│       ├── lib/
│       │   ├── api/             # typed client → /api/backend/...
│       │   ├── stubs/           # Phase 2 typed stubs (swap in Phase 5)
│       │   ├── validators/      # Zod schemas shared with forms
│       │   └── brand.ts         # CSS var names / token helpers
│       └── styles/
│           └── globals.css
└── backend/
    ├── Dockerfile
    ├── pyproject.toml           # or requirements.txt + requirements-dev.txt
    ├── alembic.ini
    ├── alembic/
    │   ├── env.py
    │   └── versions/
    ├── app/
    │   ├── main.py
    │   ├── config.py
    │   ├── deps.py
    │   ├── db.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── destination.py
    │   │   ├── trip.py
    │   │   ├── event.py
    │   │   ├── hidden_india.py
    │   │   ├── story.py
    │   │   ├── enquiry.py
    │   │   ├── contact.py
    │   │   └── user.py
    │   ├── schemas/
    │   ├── repositories/
    │   ├── services/
    │   ├── api/
    │   │   └── v1/
    │   │       ├── router.py
    │   │       ├── destinations.py
    │   │       ├── trips.py
    │   │       ├── events.py
    │   │       ├── hidden_india.py
    │   │       ├── stories.py
    │   │       ├── community.py
    │   │       ├── enquiries.py
    │   │       ├── contact.py
    │   │       └── admin.py
    │   ├── auth/
    │   │   └── admin.py         # bearer / API-key admin gate
    │   ├── storage/
    │   │   ├── base.py          # abstract StorageBackend
    │   │   └── local.py         # volume-backed impl
    │   └── seed/
    │       └── run_seed.py
    └── tests/
        ├── conftest.py
        ├── unit/
        └── api/
```

---

## 2. Docker Service Diagram (text)

```text
┌──────────── Browser ────────────┐
│  https://localhost:3000         │
│  (never sees backend:8000)      │
└───────────────┬─────────────────┘
                │
                ▼
┌──────── frontend (Next.js) ─────┐
│  :3000                          │
│  pages + /api/backend/[...path] │
│  BACKEND_INTERNAL_URL=          │
│    http://backend:8000          │
└───────────────┬─────────────────┘
                │  travel-jungle-network
                ▼
┌──────── backend (FastAPI) ──────┐
│  :8000  /api/v1/...             │
│  non-root user, healthcheck     │
└───────┬───────────────┬─────────┘
        │               │
        ▼               ▼
┌── postgres ──┐  ┌── volume: uploads ──┐
│  :5432       │  │  /data/uploads      │
│  volume: db  │  └─────────────────────┘
└──────────────┘

Compose services: frontend | backend | db
Network: travel-jungle-network
Volumes: travel-jungle-pgdata, travel-jungle-uploads
Healthchecks: db (pg_isready), backend (/health), frontend (HTTP 200 /)
```

---

## 3. ER Relationship Summary

```text
User (future-ready)
  id, email, display_name, role [visitor|admin], created_at
  ── (no hard FKs required in MVP; ready for authorship later)

Destination 1──* Trip
Destination 1──* Event
Destination 1──0..1 HiddenIndiaStory
Destination 1──* TravelStory

HiddenIndiaStory 1──* StoryImage
TravelStory 1──* StoryImage

Enquiry  *──? Trip | Destination | HiddenIndiaStory  (optional polymorphic refs via nullable FKs + source enum)
ContactMessage  (standalone)
```

### Entities (columns — essential)

| Entity | Key fields | Notes |
|--------|------------|-------|
| **Destination** | `id`, `slug` (unique), `name`, `region`, `state`, `summary`, `hero_image_url`, `editorial` JSONB, `is_published`, `is_demo`, timestamps | `editorial`: flexible blocks (pull-quotes, map notes) without schema churn |
| **Trip** | `id`, `slug`, `destination_id` FK, `title`, `summary`, `duration_days`, `itinerary` JSONB, `inclusions` JSONB, `hero_image_url`, `is_published`, `is_demo`, timestamps | **No price/availability as “live” in MVP.** Demo rows set `is_demo=true`; omit or null price fields rather than inventing numbers |
| **Event** | `id`, `slug`, `destination_id` FK nullable, `title`, `summary`, `starts_on`, `ends_on`, `location_label`, `hero_image_url`, `is_published`, `is_demo` | Dates only when verified; otherwise omit from seed |
| **HiddenIndiaStory** | `id`, `slug`, `destination_id` FK, `title`, `tagline`, `layer_discover` JSONB, `layer_experience` JSONB, `layer_explore` JSONB, `is_published`, `is_demo` | Signature 3-layer content |
| **TravelStory** | `id`, `slug`, `destination_id` FK nullable, `title`, `body_md`, `author_display`, `status` [`pending`\|`approved`\|`rejected`], `source` [`editorial`\|`community`], `is_demo` | Community path always starts `pending` |
| **StoryImage** | `id`, `travel_story_id` / `hidden_india_story_id` (one set), `url`, `alt`, `sort_order`, `credit` | |
| **Enquiry** | `id`, `name`, `email`, `phone` nullable, `message`, `source_type`, `source_id` nullable, `created_at` | Rate-limited |
| **ContactMessage** | `id`, `name`, `email`, `subject`, `message`, `created_at` | Rate-limited |
| **User** | future-ready stub table | Admin auth MVP may use env `ADMIN_API_TOKEN` without full user CRUD |

### JSONB rationale

- **`Destination.editorial`**: sparse editorial modules differ by place; JSONB avoids wide nullable columns.
- **`Trip.itinerary` / `Trip.inclusions`**: day-wise structure varies; validated at API boundary with Pydantic models, stored as JSONB.
- **`HiddenIndiaStory.layer_*`**: each layer is a structured document (headline, body, tips, media refs) — same validation pattern.

---

## 4. API Surface Summary

Base path: **`/api/v1`**. All list endpoints support `?page=&page_size=` (defaults 1 / 20, max 50). Published-only for public reads unless noted.

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/health` | public | Liveness (also mounted at app root `/health`) |
| GET | `/destinations` | public | List published destinations |
| GET | `/destinations/{slug}` | public | Destination detail |
| GET | `/trips` | public | List published trips (`?destination=` optional) |
| GET | `/trips/{slug}` | public | Trip detail |
| GET | `/events` | public | List published events |
| GET | `/events/{slug}` | public | Event detail |
| GET | `/hidden-india` | public | List Hidden India Diaries |
| GET | `/hidden-india/{slug}` | public | Diary with 3 layers |
| GET | `/stories` | public | Approved / editorial travel stories |
| GET | `/stories/{slug}` | public | Story detail |
| POST | `/community/stories` | public + rate limit | Submit community story → `pending` |
| POST | `/enquiries` | public + rate limit | Trip / destination enquiry |
| POST | `/contact` | public + rate limit | Contact form |
| POST | `/admin/login` or header gate | admin | Validate admin token (MVP: static bearer) |
| POST/PATCH/DELETE | `/admin/destinations[/{id}]` | admin | Mutate destinations |
| POST/PATCH/DELETE | `/admin/trips[/{id}]` | admin | Mutate trips |
| POST/PATCH/DELETE | `/admin/events[/{id}]` | admin | Mutate events |
| POST/PATCH/DELETE | `/admin/hidden-india[/{id}]` | admin | Mutate diaries |
| GET/PATCH | `/admin/stories` / `/{id}` | admin | Moderate community (`approve` / `reject`) |
| POST | `/admin/upload` | admin | Upload image via storage backend |

**Proxy mapping:** browser `GET /api/backend/api/v1/destinations` → Next route strips `/api/backend` → `http://backend:8000/api/v1/destinations`.

---

## 5. Security & Env Strategy

### Environment variables

| Var | Service | Notes |
|-----|---------|-------|
| `POSTGRES_USER` / `PASSWORD` / `DB` | db, backend | Compose secrets; never commit real values |
| `DATABASE_URL` | backend | `postgresql+psycopg://...@db:5432/...` |
| `BACKEND_INTERNAL_URL` | frontend | `http://backend:8000` (server-side only) |
| `ADMIN_API_TOKEN` | backend | Bearer token for admin routes (MVP) |
| `CORS_ORIGINS` | backend | Include frontend origin only |
| `RATE_LIMIT_SUBMISSIONS_PER_MIN` | backend | Default `5` |
| `UPLOAD_ROOT` | backend | `/data/uploads` |
| `SEED_DEMO` | backend | `true` in local/demo only |

### Practices

- `.env` gitignored; ship `.env.example` with placeholders only.
- Admin: `Authorization: Bearer <ADMIN_API_TOKEN>` on all mutating content routes.
- Public POST endpoints: IP-based in-memory rate limit (MVP; document Redis as future).
- Validate/sanitize Markdown body length; strip HTML on community input.
- Uploads: allowlist image MIME + max size; store under UUID paths on volume.
- No secrets in client bundle; only Next server route sees `BACKEND_INTERNAL_URL`.

---

## 6. Seed Data Policy

**File:** `docs/seed-policy.md` (authored in Phase 7; rules apply from Phase 3).

1. Every seed row that is illustrative sets `is_demo=true`.
2. **Verified-facts-only** for Hidden India seed destinations:
   - Double Decker Living Root Bridge
   - Majuli
   - Tirthan Valley
   - Ziro Valley
   - Shnongpdeng
   - Hampi  
   Copy must stick to geographically / culturally known facts; if uncertain, omit — do not invent.
3. Never invent: trip prices, guaranteed departure dates, star ratings, fake testimonials, “X seats left,” or partner logos presented as real.
4. Demo UI must surface a subtle “Demo content” affordance when `is_demo` is true (footer note or badge on detail pages — not a floating sticker on hero media).
5. Community sample stories, if any, remain `pending` or are clearly editorial `source=editorial`.

---

## 7. Open Decisions (user approval required before Phase 2)

1. **Where should the git repo live?** No GitHub environment is linked to this Project yet. Need org/user + repo URL (or approval to create `travel-jungle` under a chosen account).
2. **Monorepo vs separate repos?** **Recommendation: single monorepo `travel-jungle/`** with `frontend/` + `backend/` + Compose at root — matches Docker networking, proxy, and sequential phases. Separate repos only if teams/deploy pipelines must diverge immediately (they should not for MVP).
3. **Any changes to brand palette or page inventory before build?** Confirm palette hex values and routes: `/`, `/explore-india`, `/explore-india/[slug]`, `/trips`, `/trips/[slug]`, `/events`, `/stories`, `/community`, `/community/submit`, `/hidden-india/[slug]`, `/about`, `/contact`.

**Gate:** Phase 2 starts only after answers to (1)–(3).

---

## 8. Phase-by-Phase Task Checklists

### Phase 1 — Analysis / Architecture *(this document)*

#### Task 1.1: Lock architecture plan

**Files:**
- Create: `/cursor/stores/self/docs/architecture-plan.md` (this file)

- [ ] **Step 1:** Confirm plan covers stack, tree, Docker, ER, API, security, seed policy, open decisions, phases 2–7.
- [ ] **Step 2:** Obtain user approval on Open Decisions §7.
- [ ] **Step 3:** Only then create git repo / branch and proceed to Phase 2.

**Verify:** User sign-off recorded by coordinator; no application code exists yet.

---

### Phase 2 — Frontend scaffold + design system + pages

> Temporary typed stubs in `frontend/src/lib/stubs/*` are allowed; swap to live API client in Phase 5.

#### Task 2.1: Scaffold Next.js App Router project

**Files:**
- Create: `travel-jungle/frontend/package.json`, `tsconfig.json`, `next.config.ts`, `tailwind.config.ts`, `postcss.config.mjs`, `src/app/layout.tsx`, `src/app/page.tsx`, `src/styles/globals.css`

- [ ] **Step 1:** From monorepo root, create Next.js (TS, App Router, Tailwind, ESLint) in `frontend/`.
- [ ] **Step 2:** Pin Node LTS in `package.json` `engines` and document in README.
- [ ] **Step 3:** `npm run build` succeeds with default home page.

**Verify:** `cd travel-jungle/frontend && npm run build` → exit 0.

#### Task 2.2: Brand tokens & typography

**Files:**
- Create: `frontend/src/lib/brand.ts`
- Modify: `frontend/src/styles/globals.css`, `frontend/tailwind.config.ts`, `frontend/src/app/layout.tsx`

- [ ] **Step 1:** Define CSS variables for palette hex values exactly as Global Constraints.
- [ ] **Step 2:** Load Playfair Display + DM Sans (next/font/google).
- [ ] **Step 3:** Map Tailwind theme colors/fonts to those variables.
- [ ] **Step 4:** Apply Warm Sand page background and Jungle Green primary text in root layout.

**Verify:** Visual check of `/` — headings use Playfair, body DM Sans; no Inter/Roboto/system-only stack.

#### Task 2.3: Layout shell (Header / Footer)

**Files:**
- Create: `frontend/src/components/layout/Header.tsx`, `Footer.tsx`, `Shell.tsx`

- [ ] **Step 1:** Header with brand wordmark “Travel Jungle” as hero-level signal on home; nav links to all primary routes.
- [ ] **Step 2:** Footer with tagline “Find the Hidden. Feel the Story.” and India-only note.
- [ ] **Step 3:** Wrap pages in `Shell`.

**Verify:** Every listed route reachable from nav; mobile nav usable at 375px width.

#### Task 2.4: Typed stubs & shared Zod validators

**Files:**
- Create: `frontend/src/lib/stubs/destinations.ts`, `trips.ts`, `events.ts`, `hidden-india.ts`, `stories.ts`
- Create: `frontend/src/lib/validators/enquiry.ts`, `contact.ts`, `community-story.ts`

- [ ] **Step 1:** Define TypeScript types mirroring API schemas (slug, titles, layers, `is_demo`).
- [ ] **Step 2:** Stub arrays for 6 Hidden India destinations (facts-only copy; mark `isDemo: true`).
- [ ] **Step 3:** Zod schemas for enquiry, contact, community submit (name, email, message length limits).

**Verify:** `npx tsc --noEmit` passes; stubs export typed data used by pages.

#### Task 2.5: Page routes (static composition)

**Files:**
- Create all `src/app/**/page.tsx` routes listed in the folder tree
- Create feature components under `components/{destination,trip,event,story,hidden-india,forms}/`

- [ ] **Step 1:** Implement each page with one job per section; home hero = brand + one headline + one sentence + one CTA + full-bleed India imagery (no cards in hero; no overlay badges).
- [ ] **Step 2:** Hidden India detail page renders three layers: **Discover / Experience / Explore with Travel Jungle**.
- [ ] **Step 3:** Wire forms to RHF + Zod (client-side only; submit handlers can no-op or call stub until Phase 5).
- [ ] **Step 4:** Editorial look: cinematic photo treatment, restrained motion (2–3 intentional transitions max site-wide).

**Verify:** `npm run dev` — manually hit each route; Lighthouse/a11y smoke optional. `npm run build` passes.

#### Task 2.6: Commit Phase 2

- [ ] **Step 1:** Commit frontend scaffold with message `feat(frontend): scaffold pages and design system`.

**Phase 2 gate:** All routes render from stubs; design tokens match brand; build green.

---

### Phase 3 — Backend models / schemas / repos / services / APIs / migrations

> **TDD:** For each API resource, write failing pytest first, then implement.

#### Task 3.1: Backend project skeleton

**Files:**
- Create: `travel-jungle/backend/pyproject.toml` (or requirements*), `app/main.py`, `app/config.py`, `app/db.py`, `app/deps.py`, `tests/conftest.py`

- [ ] **Step 1:** FastAPI app with `/health` → `{"status":"ok"}`.
- [ ] **Step 2:** Settings via pydantic-settings (`DATABASE_URL`, `ADMIN_API_TOKEN`, etc.).
- [ ] **Step 3:** SQLAlchemy engine/session factory; pytest fixture with transactional test DB.

**Verify:** `pytest tests/api/test_health.py -v` PASS; `uvicorn app.main:app` serves `/health`.

#### Task 3.2: Models + Alembic

**Files:**
- Create: all `app/models/*.py`, `alembic.ini`, `alembic/env.py`, first revision under `alembic/versions/`

- [ ] **Step 1:** Implement SQLAlchemy 2.x mapped models per ER summary (`is_demo`, JSONB columns, FKs).
- [ ] **Step 2:** Alembic `env.py` imports metadata; generate initial migration.
- [ ] **Step 3:** Ensure no `create_all` in `main.py` startup.

**Verify:** `alembic upgrade head` on empty Postgres; `\dt` shows expected tables.

#### Task 3.3: Pydantic schemas + repositories + services

**Files:**
- Create: `app/schemas/*`, `app/repositories/*`, `app/services/*`

- [ ] **Step 1:** Response/create/update schemas; nested itinerary/layer models for JSONB validation.
- [ ] **Step 2:** Repository methods: list published, get by slug, admin CRUD, moderate story.
- [ ] **Step 3:** Services enforce India-only invariants and `pending` default for community.

**Verify:** Unit tests for service rules (e.g. community story status defaults to `pending`).

#### Task 3.4: Public API routers (TDD)

**Files:**
- Create: `app/api/v1/*.py`, `tests/api/test_destinations.py`, `test_trips.py`, `test_events.py`, `test_hidden_india.py`, `test_stories.py`, `test_enquiries.py`, `test_contact.py`, `test_community.py`

- [ ] **Step 1:** Write failing tests for GET list/detail and POST enquiry/contact/community.
- [ ] **Step 2:** Implement routers; mount at `/api/v1`.
- [ ] **Step 3:** Rate-limit dependency on POST submission routes.

**Verify:** `pytest tests/api -v` all PASS.

#### Task 3.5: Admin auth + admin routes + storage interface

**Files:**
- Create: `app/auth/admin.py`, `app/api/v1/admin.py`, `app/storage/base.py`, `app/storage/local.py`, `tests/api/test_admin.py`

- [ ] **Step 1:** Failing tests: mutating without bearer → 401; with token → 201/200.
- [ ] **Step 2:** Admin dependency comparing Bearer to `ADMIN_API_TOKEN`.
- [ ] **Step 3:** CRUD + story moderation + upload via `LocalStorage(UPLOAD_ROOT)`.

**Verify:** `pytest tests/api/test_admin.py -v` PASS.

#### Task 3.6: Seed script (policy-compliant)

**Files:**
- Create: `app/seed/run_seed.py`

- [ ] **Step 1:** Idempotent seed for 6 Hidden India destinations + matching `HiddenIndiaStory` layers; `is_demo=true`.
- [ ] **Step 2:** No fake prices/testimonials/ratings.
- [ ] **Step 3:** Guard with `SEED_DEMO=true`.

**Verify:** Run seed twice — no duplicate slugs; SQL shows `is_demo=true`.

#### Task 3.7: Commit Phase 3

- [ ] Commit: `feat(backend): models, alembic, v1 APIs, seed`.

**Phase 3 gate:** Migrations apply cleanly; pytest green; OpenAPI at `/docs` reflects §4.

---

### Phase 4 — Dockerization

#### Task 4.1: Backend Dockerfile

**Files:**
- Create: `travel-jungle/backend/Dockerfile`

- [ ] **Step 1:** Slim Python 3.11+ image; non-root user; install deps; copy `app/` + alembic.
- [ ] **Step 2:** CMD runs migrations then uvicorn on `8000`.
- [ ] **Step 3:** HEALTHCHECK hits `/health`.

**Verify:** `docker build -t tj-backend ./backend` succeeds.

#### Task 4.2: Frontend Dockerfile (multi-stage standalone)

**Files:**
- Create: `travel-jungle/frontend/Dockerfile`
- Modify: `frontend/next.config.ts` (`output: 'standalone'`)

- [ ] **Step 1:** deps → build → runner stages; non-root; expose 3000.
- [ ] **Step 2:** Pass `BACKEND_INTERNAL_URL` as runtime env (server).

**Verify:** `docker build -t tj-frontend ./frontend` succeeds.

#### Task 4.3: Compose stack

**Files:**
- Create: `travel-jungle/docker-compose.yml`, `.env.example`, root `.gitignore`

- [ ] **Step 1:** Services `db`, `backend`, `frontend`; network `travel-jungle-network`; volumes `travel-jungle-pgdata`, `travel-jungle-uploads`.
- [ ] **Step 2:** Healthchecks + `depends_on: condition: service_healthy`.
- [ ] **Step 3:** Publish only frontend `:3000` (and optionally backend `:8000` for local debug — document that production browser traffic stays on frontend).

**Verify:** `docker compose up --build -d` → all healthy; `curl localhost:3000` 200; `curl localhost:8000/health` 200 (if exposed).

#### Task 4.4: Commit Phase 4

- [ ] Commit: `chore: dockerize frontend, backend, compose`.

**Phase 4 gate:** Cold `compose up` yields healthy stack without manual steps beyond `.env`.

---

### Phase 5 — Integration (proxy, services, forms, images)

#### Task 5.1: Next.js backend proxy

**Files:**
- Create: `frontend/src/app/api/backend/[...path]/route.ts`

- [ ] **Step 1:** Forward GET/POST/PATCH/DELETE to `${BACKEND_INTERNAL_URL}/${path}` with query string + body + content-type.
- [ ] **Step 2:** Do not expose `BACKEND_INTERNAL_URL` to client components.
- [ ] **Step 3:** Map error status codes through.

**Verify:** From browser network tab, calls go to `/api/backend/...` only — never `http://backend:8000`.

#### Task 5.2: Typed API client; remove stub dependency from pages

**Files:**
- Create: `frontend/src/lib/api/client.ts`, resource modules under `lib/api/`
- Modify: pages/components to fetch via client
- Keep stubs only as Storybook/fallback if needed (prefer delete from production paths)

- [ ] **Step 1:** `apiGet` / `apiPost` helpers targeting `/api/backend/api/v1/...`.
- [ ] **Step 2:** Swap explore / trips / events / stories / hidden-india data sources.
- [ ] **Step 3:** Handle empty states and `is_demo` badge.

**Verify:** With compose up + seed, Hidden India pages show DB content.

#### Task 5.3: Forms → live POST endpoints

**Files:**
- Modify: `components/forms/*`

- [ ] **Step 1:** Enquiry, contact, community submit post through proxy.
- [ ] **Step 2:** Surface validation errors from Zod (client) and 422 (server).
- [ ] **Step 3:** Success confirmation UI (non-card where possible; simple text state).

**Verify:** Submit contact → row in `contact_messages`; community story → `status=pending`.

#### Task 5.4: Images

**Files:**
- Modify: storage serving strategy (backend static mount or Next image remote patterns)
- Configure: `next.config.ts` `images.remotePatterns` as needed

- [ ] **Step 1:** Seed/hero paths resolve in UI.
- [ ] **Step 2:** Admin upload writes to volume and returns URL usable by frontend.

**Verify:** Detail pages show images; upload round-trip works with admin token.

#### Task 5.5: Commit Phase 5

- [ ] Commit: `feat: integrate frontend proxy, forms, and images`.

**Phase 5 gate:** Full user journeys work against real API in Compose.

---

### Phase 6 — Testing

#### Task 6.1: Backend test hardening

**Files:**
- Expand: `backend/tests/**`

- [ ] **Step 1:** Cover authz matrix, rate limit (burst → 429), slug 404s, moderation flow.
- [ ] **Step 2:** Ensure CI-friendly `pytest` with disposable DB.

**Verify:** `pytest --cov=app --cov-report=term-missing` meets agreed floor (recommend ≥80% on services/api).

#### Task 6.2: Frontend checks

**Files:**
- Add: lint scripts; optional Playwright smoke under `frontend/e2e/`

- [ ] **Step 1:** `npm run lint` + `tsc --noEmit` clean.
- [ ] **Step 2:** Smoke: home, one Hidden India slug, contact submit (against compose).

**Verify:** Lint/typecheck exit 0; smoke script exit 0.

#### Task 6.3: Commit Phase 6

- [ ] Commit: `test: expand api coverage and frontend smoke`.

**Phase 6 gate:** Automated tests green in clean environment.

---

### Phase 7 — Documentation

#### Task 7.1: Root README + docs

**Files:**
- Create: `travel-jungle/README.md`, `docs/architecture.md`, `docs/api.md`, `docs/seed-policy.md`

- [ ] **Step 1:** README: quick start (`cp .env.example .env`, `docker compose up --build`), brand blurb, India-only scope, demo disclaimer.
- [ ] **Step 2:** architecture.md — condensed diagram + boundaries from this plan.
- [ ] **Step 3:** api.md — table from §4 + admin auth header example.
- [ ] **Step 4:** seed-policy.md — copy §6 rules.

**Verify:** Fresh contributor can bring stack up using README alone.

#### Task 7.2: Final commit

- [ ] Commit: `docs: README, architecture, API, seed policy`.

**Phase 7 gate:** MVP documentation complete; plan phases 2–7 all checked.

---

## 9. Out of Scope for MVP

| Excluded | Notes |
|----------|--------|
| Payments / booking checkout | Enquiries only |
| Redis / Kafka / Kubernetes | Compose + in-memory rate limit |
| International travel | India-only content & copy |
| S3 / cloud object storage | `StorageBackend` interface + local volume only |
| Full user accounts / OAuth | `User` table future-ready; admin via API token |
| Live pricing & availability | Never invent; omit from seed |
| Native mobile apps | Responsive web only |

---

## Execution Handoff

**Plan complete.** Saved to the Project store path required by the assignment.

After Open Decisions (§7) are answered:

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks  
2. **Inline Execution** — executing-plans in one session with checkpoints  

**Which approach — and please answer §7 before Phase 2.**
