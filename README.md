# B2Bmarket Portal – Backend

FastAPI backend for the B2B marketplace portal. Development is done with **TDD** using **pytest**.

## Setup

```bash
cd app
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
# Edit .env (e.g. DATABASE_URL for Postgres; tests use SQLite by default)
```

## Run

```bash
cd app
uvicorn main:app --reload --port 8000
```

- API: http://localhost:8000  
- Docs: http://localhost:8000/docs  

## Tests (TDD)

From the `app` directory:

```bash
cd app
python -m pytest be/tests -v
```

Tests use an in-memory SQLite DB by default so no Postgres is required for TDD.

## Migrations (Alembic)

From the `app` directory. The DB URL is taken from `config.get_settings().DATABASE_URL` (see `migrations/env.py`).

```bash
cd app
alembic revision --autogenerate -m "describe change"
alembic upgrade head
alembic downgrade -1   # optional: rollback one revision
```

## Authentication

The backend includes FastAPI authentication endpoints as an alternative to the Lambda service:

- `POST /api/auth/login` – Login with email/password, returns JWT tokens
- `POST /api/auth/refresh` – Refresh access token using refresh token
- `POST /api/auth/verify` – Verify token and get user information

**Environment Variables:**
- `JWT_SECRET` – Secret key for JWT signing (use `openssl rand -hex 32` to generate)

**Create a test user:**
```python
from be.utils.password import hash_password
from be.models.user import User
from be.database import get_db_session

with get_db_session() as db:
    user = User(
        email="admin@b2bmarket.com",
        password_hash=hash_password("your-password"),
        active=True,
        status="ACTIVE"
    )
    db.add(user)
    db.commit()
```

## Project layout

- `main.py` – FastAPI app, CORS, router registration
- `config.py` – Settings (B2Bmarket)
- `alembic.ini` – Alembic config; migrations in `migrations/`
- `be/` – Application code
  - `database.py` – SQLAlchemy engine, session, `Base`, `get_db`
  - `routers/` – API routes (ping, health, auth, vendors, …)
  - `schemas/` – **Pydantic** request/response models
  - `utils/` – Utilities (JWT, password hashing)
  - `tests/` – pytest tests and `conftest.py` fixtures
