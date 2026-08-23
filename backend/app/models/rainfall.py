"""SQLAlchemy ORM model for weather station and sensor rainfall telemetry."""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.models import Base


class RainfallReading(Base):
    """Represents rainfall telemetry observations per zone or weather station."""

    __tablename__ = "rainfall_readings"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False, index=True)
    station_name = Column(String(100), nullable=True)
    reading_timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    rainfall_1h_cm = Column(Float, nullable=False, default=0.0)
    rainfall_3h_cm = Column(Float, nullable=False, default=0.0)
    rainfall_24h_cm = Column(Float, nullable=False, default=0.0)
    rainfall_7d_cm = Column(Float, nullable=False, default=0.0)
    humidity_pct = Column(Float, nullable=True)
    temperature_c = Column(Float, nullable=True)

    # TODO: Add relationship back to Zone model
