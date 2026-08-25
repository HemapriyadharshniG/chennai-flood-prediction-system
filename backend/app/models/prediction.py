"""SQLAlchemy ORM model for model-generated flood risk predictions."""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.models import Base


class FloodPrediction(Base):
    """Represents a computed flood risk inference result for a zone."""

    __tablename__ = "flood_predictions"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False, index=True)
    prediction_timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    rainfall_input_cm = Column(Float, nullable=False)
    flood_probability = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    predicted_flood_depth_cm = Column(Float, nullable=False, default=0.0)
    model_version = Column(String(20), default="v1.0")

    # TODO: Add relationship back to Zone model
