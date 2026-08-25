"""Service layer for flood prediction inference and risk categorization."""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
import logging

from sqlalchemy.orm import Session

from app.ml.model_loader import (
    predict_flood_risk,
    get_feature_columns,
    classify_risk,
    estimate_flood_depth,
    get_recommended_action,
)
from app.models.prediction import FloodPrediction
from app.models.zone import Zone

logger = logging.getLogger(__name__)

# Drainage capacity string → numeric score mapping
DRAINAGE_SCORE_MAP = {
    "HIGH": 0.8,
    "MEDIUM": 0.5,
    "LOW": 0.2,
}


class PredictionService:
    """Orchestrates ML inference, zone feature assembly, DB persistence,
    and risk level assignment for flood predictions."""

    def __init__(self, db: Session):
        self.db = db

    def predict(self, zone_id: int, rainfall_1h_cm: float,
                rainfall_24h_cm: float, rainfall_7d_cm: float,
                humidity_pct: float = 80.0,
                reservoir_level_pct: float = 50.0) -> Dict[str, Any]:
        """Execute flood risk prediction for a given zone.

        1. Fetches zone metadata (elevation, drainage, impervious surface)
        2. Assembles full feature vector for the ML model
        3. Runs LightGBM inference (or heuristic fallback)
        4. Persists prediction record to the database
        5. Returns formatted prediction response
        """
        # Fetch zone from DB
        zone = self.db.query(Zone).filter(Zone.id == zone_id).first()
        if not zone:
            raise ValueError(f"Zone not found: {zone_id}")

        # Assemble feature dictionary matching model_metadata.json column order
        now = datetime.now(timezone.utc)
        features = {
            "rainfall_1h_cm": rainfall_1h_cm,
            "rainfall_3h_cm": rainfall_1h_cm * 2.5,  # Estimate 3h from 1h if not provided
            "rainfall_24h_cm": rainfall_24h_cm,
            "rainfall_7d_cm": rainfall_7d_cm,
            "humidity_pct": humidity_pct,
            "temperature_c": 28.0,  # Default Chennai temperature
            "month": now.month,
            "is_monsoon": 1 if now.month in (10, 11, 12) else 0,
            "avg_elevation_m": zone.avg_elevation_m or 7.0,
            "drainage_capacity_score": DRAINAGE_SCORE_MAP.get(
                (zone.drainage_capacity or "MEDIUM").upper(), 0.5
            ),
            "impervious_surface_pct": zone.impervious_surface_pct or 60.0,
            "proximity_to_water_km": zone.proximity_to_water_km or 2.0,
        }

        # Run ML inference
        result = predict_flood_risk(features)

        # Persist prediction to database
        prediction_record = FloodPrediction(
            zone_id=zone_id,
            prediction_timestamp=now,
            rainfall_input_cm=rainfall_24h_cm,
            flood_probability=result["flood_probability"],
            risk_level=result["risk_level"],
            predicted_flood_depth_cm=result["predicted_flood_depth_cm"],
            model_version="v1.0",
        )
        self.db.add(prediction_record)
        self.db.commit()

        logger.info(
            "Prediction for zone %d (%s): %.2f%% → %s",
            zone_id, zone.zone_name, result["flood_probability"] * 100, result["risk_level"]
        )

        # Build response
        return {
            "zone_id": zone_id,
            "zone_name": zone.zone_name,
            "flood_probability": result["flood_probability"],
            "risk_level": result["risk_level"],
            "predicted_flood_depth_cm": result["predicted_flood_depth_cm"],
            "recommended_action": result["recommended_action"],
            "model_type": result["model_type"],
            "timestamp": now.isoformat(),
            "input_features": {
                "rainfall_1h_cm": rainfall_1h_cm,
                "rainfall_24h_cm": rainfall_24h_cm,
                "rainfall_7d_cm": rainfall_7d_cm,
                "humidity_pct": humidity_pct,
            },
            "zone_metadata": {
                "avg_elevation_m": zone.avg_elevation_m,
                "drainage_capacity": zone.drainage_capacity,
                "impervious_surface_pct": zone.impervious_surface_pct,
                "proximity_to_water_km": zone.proximity_to_water_km,
            },
        }
