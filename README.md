# GitHub Tracker API ✅

A small FastAPI service that fetches GitHub repository information and stores it in a PostgreSQL database.

---

## 1) Problem Understanding & Assumptions 📘

**Interpretation:**
- The core requirement is a REST API that takes an owner and repository name, fetches repository metadata from GitHub, persists it in a database, and provides simple CRUD endpoints for stored repositories.

**Use Case:**
- Example: A developer wants to track popularity (stars) and quick metadata for repositories of interest (e.g., for monitoring or reporting).

**Assumptions (mandatory):**
- External API (GitHub) is reachable and responds in expected JSON structure (fields: `name`, `owner.login`, `stargazers_count`, `html_url`).
- No authentication is currently enforced for the API (the service is behind a network perimeter or used for demonstrations). If you need auth, recommend adding OAuth or API keys later.
- The application stores a single snapshot of a repository when created. Updates to `stars` are manual via the update endpoint (could be extended with a sync job).
- The database in production is PostgreSQL (the project uses `DATABASE_URL` environment variable). Tests run against Postgres as well.

---

## 2) Design Decisions 💡

### Database Schema
- Single table `repositories` with columns:
  - `id` (PK, serial)
  - `name` (text)
  - `owner` (text)
  - `stars` (integer)
  - `url` (text, unique)
- Unique constraint on `url` prevents duplicates for the same repository.
- Indexing: primary key on `id` and unique index on `url` provides efficient lookups and ensures uniqueness.

### Project Structure
- `app/`
  - `main.py` — app instance and router registration
  - `api/routes/` — route handlers (REST endpoints)
  - `core/` — `database.py` (SQLAlchemy engine/session config), exceptions
  - `crud/` — database access functions
  - `models/` — SQLAlchemy models
  - `schemas/` — Pydantic models (input/output validation)
  - `services/` — external API integrations (e.g., GitHub fetching)
- `tests/` — pytest tests and fixtures

This follows a layered structure (presentation → business → data access), which keeps responsibilities separated.

### Validation Logic
- Pydantic schemas validate input types and output shapes.
- Additional integrity checks are enforced at DB level (unique URL constraint).
- Service layer sanitizes and maps external API responses into application DTOs.

### External API Design (GitHub)
- `app/services/github_service.py` handles the HTTP request to GitHub.
- Handle **timeouts** and **network errors** by setting reasonable timeouts and propagating clear errors to callers.
- Rate limit handling: currently not implemented; recommended enhancements:
  - Use caching, retries with exponential backoff, or authenticated requests to increase rate limits.

---

## 3) Solution Approach (data flow) 🔁
1. Client POSTs to `/repositories/` with `{ owner, repo_name }`.
2. Service layer calls GitHub API to fetch repository details.
3. Service maps GitHub JSON to the app's model form and calls `crud.create_repo`.
4. Repository data stored in Postgres (`repositories` table).
5. Client can GET/PUT/DELETE entities using `/repositories/{id}` endpoints.

---

## 4) Error Handling Strategy ⚠️
- Database connectivity errors: app will raise an explicit error at startup if `DATABASE_URL` isn't set or is not Postgres; tests verify DB availability.
- GitHub errors: HTTP errors/timeouts are handled in the service; errors are returned as HTTP responses (4xx/5xx) by route handlers.
- Tests use fixtures to reset DB before each test to ensure isolation.

**Note:** Consider adding a global FastAPI exception handler to centralize formatting for errors (e.g., returning JSON {"detail": "..."} with proper HTTP status codes).

---

## 5) How to Run the Project ▶️

### Prereqs
- Python 3.10+ (3.11/3.13 used in CI/testing here)
- PostgreSQL server
- `pip` installed

### Setup (local)
1. Create and activate a virtual environment:
   - Windows (PowerShell): `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Create `.env` by copying `.env.example` and updating values:
   - `cp .env.example .env` (Windows: `copy .env.example .env`)
4. Ensure Postgres DB exists (example script provided):
   - `python scripts/create_db.py`
5. Start the app:
   - `python -m uvicorn app.main:app --reload --env-file .env --host 127.0.0.1 --port 8000`
6. Open docs:
   - http://127.0.0.1:8000/docs

### Example API call (cURL)
- Create repository:
```bash
curl -X POST "http://127.0.0.1:8000/repositories/" -H "Content-Type: application/json" -d '{"owner": "fastapi", "repo_name": "fastapi"}'
```

---

## 6) Environment Variables (.env.example) 🧾
See `.env.example` for required variables.

---

## 7) Tests
- Run tests with:
```bash
pytest -q -s
```
- Tests reset DB before each test to ensure consistent behavior.

---

## 8) Future Improvements ✨
- Add authentication (JWT or OAuth) for API endpoints
- Add background sync job to keep `stars` updated
- Add Alembic migrations for schema evolution
- Use Docker + docker-compose for local dev environment with a Postgres service

---

If you want, I can also add a CI pipeline (GitHub Actions) to run tests against Postgres and build a Docker image. 🔧

---

**Author:** GitHub Copilot (Raptor mini (Preview))
