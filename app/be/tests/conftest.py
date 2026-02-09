"""Pytest fixtures for B2Bmarket backend TDD."""
import os
import sys
from typing import Generator, Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Ensure app and config are importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from be.database import Base, get_db
from be.routers import health, ping
from config import get_settings

# Use SQLite for tests so TDD works without Postgres
TEST_DATABASE_URL = get_settings().DATABASE_UT_URL
if TEST_DATABASE_URL.startswith("postgresql"):
    TEST_DATABASE_URL = "sqlite:///./test_b2bmarket.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_test_app() -> FastAPI:
    """Build FastAPI app with routers for testing."""
    app = FastAPI()
    app.include_router(ping.router, prefix="/api")
    app.include_router(health.router, prefix="/api")
    return app


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """Create app and fresh DB for each test."""
    Base.metadata.create_all(engine)
    _app = create_test_app()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[Session, Any, None]:
    """Database session with transaction rollback after test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    if transaction.is_active:
        transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    """TestClient with get_db overridden to use test session."""

    def _get_test_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as c:
        yield c
