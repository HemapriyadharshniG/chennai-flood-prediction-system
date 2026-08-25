"""SQLAlchemy + GeoAlchemy2 ORM models package."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass
