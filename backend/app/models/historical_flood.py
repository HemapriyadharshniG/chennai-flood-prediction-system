"""SQLAlchemy ORM model for historical Chennai flood records."""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey

from app.models import Base


class HistoricalFlood(Base):
    """Represents documented historical flood events in Chennai (e.g., 2015, 2021, Michaung 2023)."""

    __tablename__ = "historical_floods"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False, index=True)
    event_date = Column(Date, nullable=False)
    event_name = Column(String(100), nullable=True)
    flood_depth_cm = Column(Float, nullable=True)
    flood_duration_hours = Column(Integer, nullable=True)
    rainfall_24h_cm = Column(Float, nullable=True)
    source = Column(String(100), nullable=True)

    # TODO: Add relationship back to Zone model
