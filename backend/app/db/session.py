"""Database engine and session management configuration."""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# Create SQLAlchemy synchronous engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

# Session factory for handling DB transactions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# TODO: Ensure PostGIS extension and GeoAlchemy2 spatial type handlers are initialized:
# e.g., with engine.connect() as conn: conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))



def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a request-scoped session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
