"""Rainfall data and weather telemetry endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["Rainfall"])


@router.get("/rainfall/current")
async def get_current_rainfall():
    """Retrieve the latest rainfall telemetry across all Chennai weather stations.

    TODO:
    - Query latest rainfall readings per zone/station from DB
    - Optionally integrate with OpenWeatherMap API for live sync
    """
    return {
        "message": "Current rainfall endpoint - returns latest rainfall readings",
        "data": [],
    }
