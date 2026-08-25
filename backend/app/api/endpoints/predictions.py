"""Flood prediction and risk inference endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import PredictionService

router = APIRouter(tags=["Predictions"])


@router.post("/predict", response_model=PredictionResponse)
async def predict_flood(request: PredictionRequest, db: Session = Depends(get_db)):
    """Generate flood risk assessment and depth prediction for a specific zone.

    Accepts rainfall parameters and a zone ID, runs the trained LightGBM model
    (or heuristic fallback), persists the prediction, and returns the result.

    Example request body:
    ```json
    {
        "zone_id": 1,
        "rainfall_1h_cm": 5.0,
        "rainfall_24h_cm": 20.0,
        "rainfall_7d_cm": 45.0,
        "humidity_pct": 92,
        "reservoir_level_pct": 85
    }
    ```
    """
    service = PredictionService(db)

    try:
        result = service.predict(
            zone_id=request.zone_id,
            rainfall_1h_cm=request.rainfall_1h_cm,
            rainfall_24h_cm=request.rainfall_24h_cm,
            rainfall_7d_cm=request.rainfall_7d_cm,
            humidity_pct=request.humidity_pct,
            reservoir_level_pct=request.reservoir_level_pct,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
