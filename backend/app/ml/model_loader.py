"""Machine Learning model loader and LightGBM inference runner.

This module handles loading serialized LightGBM model artifacts (.pkl files)
from disk, preparing tabular feature vectors, performing inference, and executing
domain-specific heuristic fallbacks when model artifacts are absent.
"""

from typing import Dict, Any, Optional
import os
import json
import logging

import joblib
import numpy as np

logger = logging.getLogger(__name__)

# ── Resolve model paths relative to this file ────────────────────────────
_ML_DIR = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH = os.path.join(_ML_DIR, "lightgbm_flood_model.pkl")
_METADATA_PATH = os.path.join(_ML_DIR, "model_metadata.json")

# ── Module-level singleton: loaded once on first call ────────────────────
_model = None
_metadata = None
_is_loaded = False


def _ensure_loaded() -> None:
    """Lazy-load model and metadata on first inference call."""
    global _model, _metadata, _is_loaded
    if _is_loaded:
        return

    # Load metadata (feature column order + risk thresholds)
    if os.path.exists(_METADATA_PATH):
        with open(_METADATA_PATH, "r") as f:
            _metadata = json.load(f)
        logger.info("Loaded model metadata: %d features", len(_metadata["feature_columns"]))
    else:
        logger.warning("Model metadata not found at %s", _METADATA_PATH)
        _metadata = None

    # Load trained LightGBM model
    if os.path.exists(_MODEL_PATH):
        _model = joblib.load(_MODEL_PATH)
        logger.info("Loaded LightGBM model from %s", _MODEL_PATH)
    else:
        logger.warning("No trained model found at %s — will use heuristic fallback", _MODEL_PATH)
        _model = None

    _is_loaded = True


def get_feature_columns() -> list:
    """Return the ordered list of feature column names the model expects."""
    _ensure_loaded()
    if _metadata:
        return _metadata["feature_columns"]
    # Fallback default order if metadata is missing
    return [
        "rainfall_1h_cm", "rainfall_3h_cm", "rainfall_24h_cm", "rainfall_7d_cm",
        "humidity_pct", "temperature_c", "month", "is_monsoon",
        "avg_elevation_m", "drainage_capacity_score", "impervious_surface_pct",
        "proximity_to_water_km",
    ]


def get_risk_thresholds() -> Dict[str, float]:
    """Return probability thresholds for risk classification."""
    _ensure_loaded()
    if _metadata and "risk_thresholds" in _metadata:
        return _metadata["risk_thresholds"]
    return {"LOW": 0.25, "MODERATE": 0.55, "HIGH": 0.80, "CRITICAL": 1.0}


def classify_risk(probability: float) -> str:
    """Map a flood probability (0.0–1.0) to a risk level string."""
    thresholds = get_risk_thresholds()
    if probability < thresholds["LOW"]:
        return "LOW"
    elif probability < thresholds["MODERATE"]:
        return "MODERATE"
    elif probability < thresholds["HIGH"]:
        return "HIGH"
    return "CRITICAL"


def estimate_flood_depth(probability: float) -> float:
    """Estimate standing water depth (cm) from flood probability.

    Simple linear mapping: probability * 100 gives estimated depth.
    E.g., 0.75 probability → ~75 cm estimated flood depth.
    """
    return round(probability * 100.0, 2)


def get_recommended_action(risk_level: str) -> str:
    """Return citizen safety recommendation based on risk level."""
    actions = {
        "LOW": "Normal conditions. No immediate action required.",
        "MODERATE": "Stay alert. Monitor weather updates and avoid waterlogging-prone areas.",
        "HIGH": "Avoid low-lying streets. Move vehicles to higher ground. Keep emergency kit ready.",
        "CRITICAL": "EVACUATE low-lying areas immediately. Contact NDMA helpline 1078. Move to higher floors.",
    }
    return actions.get(risk_level, "Monitor weather conditions.")


def predict_flood_risk(features: Dict[str, Any]) -> Dict[str, Any]:
    """Perform flood risk prediction using the trained LightGBM model.

    Args:
        features: Dictionary containing all required feature values.
                  Keys must match the feature_columns from model_metadata.json.

    Returns:
        Dict with flood_probability, risk_level, predicted_flood_depth_cm,
        recommended_action, and model_type.
    """
    _ensure_loaded()

    if _model is not None:
        # Build feature vector in the exact column order the model expects
        feature_cols = get_feature_columns()
        feature_vector = np.array([[features.get(col, 0.0) for col in feature_cols]])

        # LightGBM predict_proba returns [[p_no_flood, p_flood]]
        probability = float(_model.predict_proba(feature_vector)[0][1])

        return {
            "flood_probability": round(probability, 4),
            "risk_level": classify_risk(probability),
            "predicted_flood_depth_cm": estimate_flood_depth(probability),
            "recommended_action": get_recommended_action(classify_risk(probability)),
            "model_type": "lightgbm",
        }
    else:
        # Fallback to heuristic when model file is not available
        return heuristic_fallback(features)


def heuristic_fallback(features: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based heuristic flood risk assessment when ML model is unavailable.

    Uses weighted scoring based on rainfall intensity, elevation,
    drainage capacity, and surface imperviousness.
    """
    score = 0.0

    # Rainfall contributions (heaviest weight)
    r1h = features.get("rainfall_1h_cm", 0.0)
    r24h = features.get("rainfall_24h_cm", 0.0)
    r7d = features.get("rainfall_7d_cm", 0.0)
    score += min(r1h / 10.0, 0.30)
    score += min(r24h / 30.0, 0.30)
    score += min(r7d / 80.0, 0.15)

    # Elevation penalty (lower = more flood-prone)
    elevation = features.get("avg_elevation_m", 10.0)
    score += max(0.0, (10.0 - elevation) / 40.0)

    # Impervious surface contribution
    impervious = features.get("impervious_surface_pct", 50.0)
    score += (impervious / 100.0) * 0.15

    # Drainage penalty
    drainage = features.get("drainage_capacity_score", 0.5)
    score += (1.0 - drainage) * 0.10

    probability = round(min(max(score, 0.0), 1.0), 4)
    risk_level = classify_risk(probability)

    return {
        "flood_probability": probability,
        "risk_level": risk_level,
        "predicted_flood_depth_cm": estimate_flood_depth(probability),
        "recommended_action": get_recommended_action(risk_level),
        "model_type": "heuristic_fallback",
    }
