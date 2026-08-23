"""SQLAlchemy ORM model for streets, roads, and flood-prone underpasses."""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from geoalchemy2 import Geometry

from app.models import Base


class Street(Base):
    """Represents a street segment or underpass in Chennai with spatial line geometry."""

    __tablename__ = "streets"

    id = Column(Integer, primary_key=True, index=True)
    street_name = Column(String(150), nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False, index=True)
    geometry = Column(Geometry("LINESTRING", srid=4326), nullable=False)
    is_underpass = Column(Boolean, default=False, nullable=False)
    elevation_m = Column(Float, nullable=True)

    # TODO: Add relationship back to Zone model
