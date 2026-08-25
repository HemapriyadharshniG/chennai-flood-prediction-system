"""Service layer for Chennai zone spatial queries and GeoJSON formatting.

PostGIS does the GeoJSON serialisation via ST_AsGeoJSON — geometry is never
parsed into Python objects, only json.loads() on the string PostGIS returns.
The latest risk overlay comes from a LATERAL join on flood_predictions so one
round trip serves the whole map layer.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional, Sequence

from geoalchemy2.functions import (
    ST_AsGeoJSON,
    ST_Contains,
    ST_Extent,
    ST_Intersects,
    ST_MakeEnvelope,
    ST_MakePoint,
    ST_SetSRID,
    ST_SimplifyPreserveTopology,
)
from sqlalchemy import Row, select, true
from sqlalchemy.orm import Session

from app.models.prediction import FloodPrediction
from app.models.zone import Zone
from app.schemas.zone import ZoneFeature, ZoneFeatureCollection, ZoneProperties

logger = logging.getLogger(__name__)

SRID = 4326

# 6 decimals is ~0.11 m — far past street-level need, and roughly a third the
# payload of the 15-digit default.
GEOJSON_PRECISION = 6


class ZoneService:
    """Handles spatial queries and business logic for administrative zones."""

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------ #
    # Query construction
    # ------------------------------------------------------------------ #

    @staticmethod
    def _latest_prediction():
        """LATERAL subquery: newest flood_predictions row per zone."""
        return (
            select(
                FloodPrediction.risk_level,
                FloodPrediction.flood_probability,
                FloodPrediction.predicted_flood_depth_cm,
                FloodPrediction.prediction_timestamp,
                FloodPrediction.model_version,
            )
            .where(FloodPrediction.zone_id == Zone.id)
            .order_by(FloodPrediction.prediction_timestamp.desc())
            .limit(1)
            .lateral("latest_prediction")
        )

    @staticmethod
    def _geometry_expr(simplify_tolerance: Optional[float]):
        """Optionally generalise polygons before serialising (degrees, EPSG:4326)."""
        if simplify_tolerance and simplify_tolerance > 0:
            return ST_SimplifyPreserveTopology(Zone.geometry, simplify_tolerance)
        return Zone.geometry

    @staticmethod
    def _envelope(bbox: Sequence[float]):
        if len(bbox) != 4:
            raise ValueError("bbox must be minLon,minLat,maxLon,maxLat")
        min_lon, min_lat, max_lon, max_lat = (float(v) for v in bbox)
        if min_lon >= max_lon or min_lat >= max_lat:
            raise ValueError("bbox minimum values must be smaller than maximum values")
        return ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, SRID)

    def _base_statement(self, simplify_tolerance: Optional[float] = None):
        """Return (statement, lateral).

        The lateral is handed back so callers can filter on its columns —
        referencing a freshly built one would join flood_predictions twice.
        """
        latest = self._latest_prediction()
        stmt = (
            select(
                Zone.id,
                Zone.zone_name,
                Zone.ward_number,
                Zone.area_sqkm,
                Zone.avg_elevation_m,
                Zone.drainage_capacity,
                Zone.land_use,
                Zone.impervious_surface_pct,
                Zone.proximity_to_water_km,
                ST_AsGeoJSON(
                    self._geometry_expr(simplify_tolerance), GEOJSON_PRECISION
                ).label("geometry_geojson"),
                latest.c.risk_level,
                latest.c.flood_probability,
                latest.c.predicted_flood_depth_cm,
                latest.c.prediction_timestamp,
                latest.c.model_version,
            )
            # outer join keeps zones that have never been scored
            .outerjoin(latest, true())
        )
        return stmt, latest

    # ------------------------------------------------------------------ #
    # Row mapping
    # ------------------------------------------------------------------ #

    @staticmethod
    def _to_feature(row: Row) -> ZoneFeature:
        geometry: Dict[str, Any] = json.loads(row.geometry_geojson)
        timestamp = row.prediction_timestamp
        return ZoneFeature(
            id=row.id,
            geometry=geometry,
            properties=ZoneProperties(
                id=row.id,
                zone_name=row.zone_name,
                ward_number=row.ward_number,
                area_sqkm=row.area_sqkm,
                avg_elevation_m=row.avg_elevation_m,
                drainage_capacity=row.drainage_capacity,
                land_use=row.land_use,
                impervious_surface_pct=row.impervious_surface_pct,
                proximity_to_water_km=row.proximity_to_water_km,
                risk_level=row.risk_level,
                flood_probability=row.flood_probability,
                predicted_flood_depth_cm=row.predicted_flood_depth_cm,
                prediction_timestamp=timestamp.isoformat() if timestamp else None,
                model_version=row.model_version,
            ),
        )

    def _extent(self, bbox: Optional[Sequence[float]]) -> Optional[List[float]]:
        """[minLon, minLat, maxLon, maxLat] for the selected zones."""
        stmt = select(ST_Extent(Zone.geometry))
        if bbox:
            stmt = stmt.where(ST_Intersects(Zone.geometry, self._envelope(bbox)))
        raw = self.db.execute(stmt).scalar()
        if not raw:
            return None
        # PostGIS returns 'BOX(minx miny,maxx maxy)'
        inner = raw[raw.index("(") + 1 : raw.index(")")]
        lower, upper = inner.split(",")
        min_lon, min_lat = (float(v) for v in lower.split())
        max_lon, max_lat = (float(v) for v in upper.split())
        return [min_lon, min_lat, max_lon, max_lat]

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def get_zones_geojson(
        self,
        *,
        bbox: Optional[Sequence[float]] = None,
        risk_level: Optional[str] = None,
        simplify_tolerance: Optional[float] = None,
    ) -> ZoneFeatureCollection:
        """All zones as a GeoJSON FeatureCollection for the Leaflet layer.

        bbox filters with ST_Intersects so the GiST index on zones.geometry
        is used rather than a sequential scan.
        """
        stmt, latest = self._base_statement(simplify_tolerance)

        if bbox:
            stmt = stmt.where(ST_Intersects(Zone.geometry, self._envelope(bbox)))
        if risk_level:
            stmt = stmt.where(latest.c.risk_level == risk_level.upper())

        rows = self.db.execute(stmt.order_by(Zone.zone_name)).all()
        logger.debug("get_zones_geojson -> %d features (bbox=%s)", len(rows), bbox)

        return ZoneFeatureCollection(
            features=[self._to_feature(r) for r in rows],
            bbox=self._extent(bbox),
        )

    def get_zone_geojson(self, zone_id: int) -> Optional[ZoneFeature]:
        """One zone as a GeoJSON Feature, or None if the id is unknown."""
        stmt, _ = self._base_statement()
        row = self.db.execute(stmt.where(Zone.id == zone_id)).first()
        return self._to_feature(row) if row else None

    def get_zone_at_point(self, lat: float, lon: float) -> Optional[ZoneFeature]:
        """Point-in-polygon lookup for map taps."""
        # ST_MakePoint is (x=lon, y=lat) — order matters.
        point = ST_SetSRID(ST_MakePoint(lon, lat), SRID)
        stmt, _ = self._base_statement()
        stmt = stmt.where(ST_Contains(Zone.geometry, point)).limit(1)
        row = self.db.execute(stmt).first()
        return self._to_feature(row) if row else None

    def get_zones_for_scoring(
        self, zone_ids: Optional[Sequence[int]] = None
    ) -> List[Zone]:
        """Zone rows without geometry, for the risk model."""
        stmt = select(Zone)
        if zone_ids:
            stmt = stmt.where(Zone.id.in_(list(zone_ids)))
        return list(self.db.execute(stmt.order_by(Zone.zone_name)).scalars().all())
