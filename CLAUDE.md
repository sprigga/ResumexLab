# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ResumeXLab is a full-stack resume management system with a FastAPI backend (SQLite/SQLAlchemy), Vue 3 frontend (Pinia + Element Plus), and Docker-based deployment. It supports bilingual content (Traditional Chinese / English) and JWT authentication.

## Commands

### Backend (from `backend/`)
```bash
# Environment setup
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Run dev server (http://localhost:8000)
python run.py
# OR: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/
pytest tests/test_auth_required.py  # single test file

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "description"
```

### Frontend (from `frontend/`)
```bash
npm install
npm run dev    # http://localhost:5173 (proxies /api to :8000)
npm run build
```

### Docker
```bash
# Production (ports 58432/58433)
docker-compose up -d --build

# Development (ports 8000/8001)
docker-compose -f docker-compose.dev.yml up -d
```

## Architecture

### Three Factory Patterns (Core Design)

The codebase uses three parallel factory patterns that eliminate boilerplate:

1. **Backend CRUD Router Factory** — `backend/app/api/crud_base.py`  
   `create_crud_router(model, schemas, ...)` generates all 5 REST endpoints (GET list, GET by id, POST, PUT, DELETE). New entities need ~10 lines total in their endpoint file.

2. **Frontend API Factory** — `frontend/src/api/createCrudApi.js`  
   `createCrudApi('entity-path')` returns `{ getAll, get, create, update, delete }`. Add an entity by calling this factory once.

3. **Frontend CRUD Composable** — `frontend/src/composables/useCrudPanel.js`  
   `useCrudPanel({ defaultForm, fetch, create, update, delete, entityName })` manages dialog state, form data, loading, and CRUD handlers. Reduces component scripts from ~100 lines to ~15.

4. **Pinia Store Factory** — `frontend/src/stores/crudFactory.js`  
   `createEntityActions(items, api)` provides `fetchAll`, `create`, `update`, `remove` with loading/error state.

### Backend Structure
```
backend/app/
├── api/
│   ├── crud_base.py        # CRUD router factory
│   ├── upload_utils.py     # File upload helpers
│   └── endpoints/          # auth, personal_info, work_experience, projects, education, ...
├── core/
│   ├── config.py           # Settings from environment variables
│   └── security.py         # JWT (HS256) + bcrypt password hashing
├── models/                 # SQLAlchemy ORM models
├── schemas/                # Pydantic v2 validation models
├── db/
│   ├── base.py             # SQLAlchemy engine, SessionLocal, Base
│   └── init_db.py          # Creates default admin user on first run
└── main.py                 # App init, router includes, CORS, middleware
```

### Frontend Structure
```
frontend/src/
├── api/
│   ├── axios.js            # Axios client: JWT interceptor, auto-retry on 5xx, 401→login
│   ├── createCrudApi.js    # API factory
│   └── resume.js           # Resume-specific API calls
├── composables/
│   └── useCrudPanel.js     # CRUD UI composable
├── stores/
│   ├── auth.js             # Auth state + token
│   ├── crudFactory.js      # Store factory
│   └── resume.js           # Central resume data store
├── views/
│   ├── ResumeView.vue      # Public resume display
│   └── admin/              # Edit views (one per entity)
└── locales/
    ├── zh-TW.js            # Traditional Chinese
    └── en-US.js            # English
```

### Database
- **SQLite** at `./backend/data/resume.db`
- **Alembic** for migrations — runs automatically on Docker startup via `entrypoint.sh`
- Migrations use `CREATE TABLE IF NOT EXISTS` for safe re-execution
- All bilingual fields are suffixed `_zh` / `_en` (e.g., `school_zh`, `school_en`)

### Authentication
- JWT tokens (HS256, 24-hour expiry) via `python-jose`
- POST `/api/auth/login` — OAuth2 password flow
- Protected endpoints require `Depends(get_current_user)`
- Public endpoints: all GET routes for resume content

### Environment Variables (required in `backend/.env`)
```
ADMIN_USERNAME=...
ADMIN_PASSWORD=...
SECRET_KEY=...
```
No hardcoded defaults for credentials — app will fail to start without these.

## Code Conventions

### Adding a New Entity
1. Create SQLAlchemy model in `backend/app/models/`
2. Create Pydantic schemas in `backend/app/schemas/`
3. Create endpoint file using `create_crud_router(...)` in `backend/app/api/endpoints/`
4. Register router in `backend/app/main.py`
5. Create Alembic migration
6. Add API instance via `createCrudApi('entity-path')` in frontend
7. Add store actions via `createEntityActions` in `frontend/src/stores/resume.js`
8. Create Edit view using `useCrudPanel` composable

### File Uploads
- Supported on work_experience + projects
- 100MB limit enforced at Nginx level
- Stored in `./backend/uploads/`
- Use `upload_utils.py` for handling

### Code Modification Policy
When modifying existing code, **comment out old code** rather than deleting, with a date and reason. This is a project preference for traceability.

## Development Notes
- Backend is optimized for GCP e2-micro (1GB RAM): single Uvicorn worker, 20-request concurrency limit
- The existing `docs/CLAUDE.md` is outdated (written before full stack was built) — this root CLAUDE.md supersedes it
- Utility scripts go in `script/` directory
- Always use `uv` for Python environment management
