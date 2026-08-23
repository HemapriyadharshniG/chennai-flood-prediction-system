"""Pydantic models for flood prediction requests and responses."""

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Input payload for single zone flood risk prediction."""

    zone_id: int = Field(..., description="Unique zone identifier")
    rainfall_1h_cm: float = Field(..., description="Observed/forecast 1-hour rainfall in cm")
    rainfall_24h_cm: float = Field(..., description="Observed/forecast 24-hour rainfall in cm")
    rainfall_7d_cm: float = Field(..., description="Observed/forecast 7-day cumulative rainfall in cm")
    humidity_pct: float = Field(80.0, description="Relative humidity percentage")
    reservoir_level_pct: float = Field(50.0, description="Average surrounding reservoir storage level percentage")


class PredictionResponse(BaseModel):
    """Output schema for computed flood risk prediction."""

    zone_id: int
    zone_name: str
    flood_probability: float
    risk_level: str
    predicted_flood_depth_cm: float
    recommended_action: str
    timestamp: str
