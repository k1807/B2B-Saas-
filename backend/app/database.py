"""Database connection and session management.

Uses DATABASE_URL from config (e.g. postgresql://user:pass@host:5432/dbname).
Tables are created on app startup in main.py.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

connect_args = {}
engine_kwargs = {"connect_args": connect_args}

if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    # PostgreSQL: reconnect on stale connections
    engine_kwargs["pool_pre_ping"] = True

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides a DB session. Closes after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
