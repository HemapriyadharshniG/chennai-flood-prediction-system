-- Chennai Flood Prediction System — Database Initialization
-- PostgreSQL + PostGIS

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- ============================================================
-- ZONES TABLE — Chennai ward/zone level polygons
-- ============================================================
CREATE TABLE IF NOT EXISTS zones (
    id SERIAL PRIMARY KEY,
    zone_name VARCHAR(100) NOT NULL,
    ward_number INTEGER,
    geometry GEOMETRY(POLYGON, 4326),
    area_sqkm FLOAT,
    avg_elevation_m FLOAT,
    drainage_capacity VARCHAR(20) DEFAULT 'MEDIUM',
    land_use VARCHAR(50) DEFAULT 'RESIDENTIAL',
    impervious_surface_pct FLOAT DEFAULT 50.0,
    proximity_to_water_km FLOAT DEFAULT 5.0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- STREETS TABLE — street-level granular data
-- ============================================================
CREATE TABLE IF NOT EXISTS streets (
    id SERIAL PRIMARY KEY,
    street_name VARCHAR(200) NOT NULL,
    zone_id INTEGER REFERENCES zones(id),
    geometry GEOMETRY(LINESTRING, 4326),
    is_underpass BOOLEAN DEFAULT FALSE,
    elevation_m FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- RAINFALL READINGS TABLE — from IMD / weather stations
-- ============================================================
CREATE TABLE IF NOT EXISTS rainfall_readings (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER REFERENCES zones(id),
    station_name VARCHAR(100),
    reading_timestamp TIMESTAMP,
    rainfall_1h_cm FLOAT,
    rainfall_3h_cm FLOAT,
    rainfall_24h_cm FLOAT,
    rainfall_7d_cm FLOAT,
    humidity_pct FLOAT,
    temperature_c FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- FLOOD PREDICTIONS TABLE — ML model outputs
-- ============================================================
CREATE TABLE IF NOT EXISTS flood_predictions (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER REFERENCES zones(id),
    prediction_timestamp TIMESTAMP,
    rainfall_input_cm FLOAT,
    flood_probability FLOAT,
    risk_level VARCHAR(20),
    predicted_flood_depth_cm FLOAT,
    model_version VARCHAR(20) DEFAULT 'v1.0',
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- HISTORICAL FLOODS TABLE — ground truth records
-- ============================================================
CREATE TABLE IF NOT EXISTS historical_floods (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER REFERENCES zones(id),
    event_date DATE,
    event_name VARCHAR(100),
    flood_depth_cm FLOAT,
    flood_duration_hours INTEGER,
    rainfall_24h_cm FLOAT,
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- SPATIAL INDEXES for fast geographic queries
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_zones_geometry ON zones USING GIST(geometry);
CREATE INDEX IF NOT EXISTS idx_streets_geometry ON streets USING GIST(geometry);
CREATE INDEX IF NOT EXISTS idx_rainfall_zone ON rainfall_readings(zone_id);
CREATE INDEX IF NOT EXISTS idx_rainfall_timestamp ON rainfall_readings(reading_timestamp);
CREATE INDEX IF NOT EXISTS idx_predictions_zone ON flood_predictions(zone_id);
CREATE INDEX IF NOT EXISTS idx_predictions_timestamp ON flood_predictions(prediction_timestamp);
CREATE INDEX IF NOT EXISTS idx_historical_zone ON historical_floods(zone_id);
CREATE INDEX IF NOT EXISTS idx_historical_date ON historical_floods(event_date);
