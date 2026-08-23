"""Street-level vulnerability and underpass monitoring endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["Streets"])


@router.get("/streets")
async def get_streets():
    """Retrieve street networks and critical underpasses vulnerable to waterlogging.

    TODO:
    - Query spatial streets table using GeoAlchemy2
    - Return street line geometries and underpass flood risk status
    """
    return {
        "message": "Streets endpoint - returns road network and underpass flood vulnerabilities",
        "data": [],
    }
