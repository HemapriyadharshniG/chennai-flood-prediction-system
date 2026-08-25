"""Historical flood event endpoints."""

from typing import Optional
from fastapi import APIRouter, Query

router = APIRouter(tags=["History"])


@router.get("/history")
async def get_flood_history(
    zone_id: Optional[int] = Query(None, description="Optional zone ID to filter history")
):
    """Retrieve historical Chennai flood events, inundation depths, and rainfall records.

    TODO:
    - Query historical_floods table optionally filtered by zone_id
    - Return list of past flood events (e.g., 2015, 2021, 2023 Michaung)
    """
    return {
        "message": "Flood history endpoint - returns past inundation records",
        "zone_id": zone_id,
        "data": [],
    }
