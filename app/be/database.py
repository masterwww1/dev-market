"""Database configuration and session management for B2Bmarket backend."""
from contextlib import contextmanager

from config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine(
    get_settings().DATABASE_URL,
    pool_size=5,
    max_overflow=5,
    pool_pre_ping=True,
    echo=get_settings().DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_db_session() -> Session:
    """Context manager for database sessions (e.g. crons, scripts)."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
