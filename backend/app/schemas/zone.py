"""GeoJSON schemas for the zones layer.

Field names mirror `database/init.sql` exactly so the frontend can read
properties straight off the table columns.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class ZoneProperties(BaseModel):
    """Feature properties: static zone attributes plus the latest risk overlay."""

    id: int
    zone_name: str
    ward_number: Optional[int] = None
    area_sqkm: Optional[float] = None
    avg_elevation_m: Optional[float] = None
    drainage_capacity: Optional[str] = None
    land_use: Optional[str] = None
    impervious_surface_pct: Optional[float] = None
    proximity_to_water_km: Optional[float] = None

    # Joined from the most recent flood_predictions row for this zone.
    risk_level: Optional[str] = None
    flood_probability: Optional[float] = None
    predicted_flood_depth_cm: Optional[float] = None
    prediction_timestamp: Optional[str] = None
    model_version: Optional[str] = None


class ZoneFeature(BaseModel):
    type: Literal["Feature"] = "Feature"
    id: int
    geometry: Dict[str, Any] = Field(
        ..., description="GeoJSON Polygon from PostGIS ST_AsGeoJSON (EPSG:4326)."
    )
    properties: ZoneProperties


class ZoneFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[ZoneFeature]
    bbox: Optional[List[float]] = Field(
        default=None, description="[minLon, minLat, maxLon, maxLat] of the returned features."
    )
