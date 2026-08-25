"""Zone endpoints — GeoJSON FeatureCollection for the Leaflet map layer.

Thin FastAPI layer over ZoneService: parses/validates query params, then
hands off to the service for the actual PostGIS queries.
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.zone import ZoneFeature, ZoneFeatureCollection
from app.services.zone_service import ZoneService

router = APIRouter(tags=["Zones"])

# Keep in sync with model_metadata.json risk_thresholds bands.
RISK_LEVEL_PATTERN = r"^(LOW|MODERATE|HIGH|CRITICAL)$"


def _parse_bbox(bbox: Optional[str]) -> Optional[List[float]]:
    """'minLon,minLat,maxLon,maxLat' -> [float, float, float, float]."""
    if bbox is None:
        return None
    parts = bbox.split(",")
    if len(parts) != 4:
        raise HTTPException(
            status_code=400, detail="bbox must be 'minLon,minLat,maxLon,maxLat'"
        )
    try:
        return [float(p) for p in parts]
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="bbox values must be numeric") from exc


@router.get("/zones", response_model=ZoneFeatureCollection)
async def get_zones(
    bbox: Optional[str] = Query(
        None,
        description="minLon,minLat,maxLon,maxLat — restricts to zones intersecting this envelope",
    ),
    risk_level: Optional[str] = Query(
        None, pattern=RISK_LEVEL_PATTERN, description="Filter by latest risk_level"
    ),
    simplify: Optional[float] = Query(
        None, ge=0, description="ST_SimplifyPreserveTopology tolerance, in degrees"
    ),
    db: Session = Depends(get_db),
) -> ZoneFeatureCollection:
    """All Chennai zones as a GeoJSON FeatureCollection, latest risk overlay joined in."""
    service = ZoneService(db)
    try:
        return service.get_zones_geojson(
            bbox=_parse_bbox(bbox), risk_level=risk_level, simplify_tolerance=simplify
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/zones/at-point", response_model=ZoneFeature)
async def get_zone_at_point(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    db: Session = Depends(get_db),
) -> ZoneFeature:
    """Point-in-polygon lookup for a tapped map coordinate."""
    service = ZoneService(db)
    feature = service.get_zone_at_point(lat=lat, lon=lon)
    if feature is None:
        raise HTTPException(status_code=404, detail="No zone contains this point")
    return feature


@router.get("/zones/{zone_id}", response_model=ZoneFeature)
async def get_zone(zone_id: int, db: Session = Depends(get_db)) -> ZoneFeature:
    """A single zone as a GeoJSON Feature."""
    service = ZoneService(db)
    feature = service.get_zone_geojson(zone_id)
    if feature is None:
        raise HTTPException(status_code=404, detail=f"Zone {zone_id} not found")
    return feature
