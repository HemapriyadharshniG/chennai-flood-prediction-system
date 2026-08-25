"""Pydantic models for flood prediction requests and responses."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Input payload for single zone flood risk prediction."""

    zone_id: int = Field(..., description="Unique zone identifier")
    rainfall_1h_cm: float = Field(..., ge=0, description="Observed/forecast 1-hour rainfall in cm")
    rainfall_24h_cm: float = Field(..., ge=0, description="Observed/forecast 24-hour rainfall in cm")
    rainfall_7d_cm: float = Field(..., ge=0, description="Observed/forecast 7-day cumulative rainfall in cm")
    humidity_pct: float = Field(80.0, ge=0, le=100, description="Relative humidity percentage")
    reservoir_level_pct: float = Field(50.0, ge=0, le=100, description="Average surrounding reservoir storage level percentage")

    model_config = {"json_schema_extra": {
        "examples": [{
            "zone_id": 1,
            "rainfall_1h_cm": 5.0,
            "rainfall_24h_cm": 20.0,
            "rainfall_7d_cm": 45.0,
            "humidity_pct": 92.0,
            "reservoir_level_pct": 85.0,
        }]
    }}


class PredictionResponse(BaseModel):
    """Output schema for computed flood risk prediction."""

    zone_id: int
    zone_name: str
    flood_probability: float = Field(..., description="Probability of flooding (0.0 to 1.0)")
    risk_level: str = Field(..., description="Risk classification: LOW, MODERATE, HIGH, or CRITICAL")
    predicted_flood_depth_cm: float = Field(..., description="Estimated standing water depth in cm")
    recommended_action: str = Field(..., description="Safety recommendation for citizens")
    model_type: str = Field(..., description="Model used: 'lightgbm' or 'heuristic_fallback'")
    timestamp: str = Field(..., description="ISO 8601 prediction timestamp")
    input_features: Optional[Dict[str, Any]] = Field(None, description="Echo of input rainfall parameters")
    zone_metadata: Optional[Dict[str, Any]] = Field(None, description="Zone elevation, drainage, and surface data used")
