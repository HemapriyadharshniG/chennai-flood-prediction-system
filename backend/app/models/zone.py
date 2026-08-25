"""SQLAlchemy ORM model for Chennai administrative and hydrological zones."""

from sqlalchemy import Column, Integer, String, Float
from geoalchemy2 import Geometry

from app.models import Base


class Zone(Base):
    """Represents a Chennai administrative/flood analysis zone with spatial boundary."""

    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String(100), nullable=False)
    ward_number = Column(Integer, nullable=True)
    geometry = Column(Geometry("POLYGON", srid=4326), nullable=False)
    area_sqkm = Column(Float, nullable=True)
    avg_elevation_m = Column(Float, nullable=True)
    drainage_capacity = Column(String(20), default="MEDIUM")
    land_use = Column(String(50), nullable=True)
    impervious_surface_pct = Column(Float, nullable=True)
    proximity_to_water_km = Column(Float, nullable=True)

    # TODO: Add relationship to rainfall_readings, flood_predictions, and streets
