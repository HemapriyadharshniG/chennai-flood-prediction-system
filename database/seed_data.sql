-- Chennai Flood Prediction System — Seed Data
-- Inserts baseline zone data for 15 Chennai zones
-- Spatial polygon data will be populated during GIS pipeline processing

-- ============================================================
-- ZONE SEED DATA — 15 Chennai Administrative Zones
-- ============================================================
INSERT INTO zones (zone_name, ward_number, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km) VALUES
('Adyar',           1,  12.5, 4.2,  'LOW',    'RESIDENTIAL',  72.0, 0.3),
('Velachery',       2,  15.3, 5.8,  'LOW',    'RESIDENTIAL',  68.0, 1.2),
('T. Nagar',        3,   8.7, 8.5,  'MEDIUM', 'COMMERCIAL',   82.0, 2.5),
('Mylapore',        4,  10.2, 6.3,  'MEDIUM', 'RESIDENTIAL',  70.0, 1.0),
('Nungambakkam',    5,   7.8, 9.1,  'MEDIUM', 'COMMERCIAL',   78.0, 2.8),
('Anna Nagar',      6,  14.1, 11.2, 'HIGH',   'RESIDENTIAL',  65.0, 3.5),
('Porur',           7,  18.4, 6.0,  'LOW',    'MIXED',        55.0, 0.8),
('Tambaram',        8,  22.6, 12.5, 'MEDIUM', 'RESIDENTIAL',  48.0, 2.0),
('Chromepet',       9,  11.3, 10.8, 'MEDIUM', 'INDUSTRIAL',   60.0, 3.2),
('Guindy',         10,   9.5, 7.5,  'MEDIUM', 'INDUSTRIAL',   75.0, 1.5),
('Kodambakkam',    11,   6.8, 8.0,  'MEDIUM', 'RESIDENTIAL',  73.0, 2.0),
('Sholinganallur', 12,  25.7, 3.5,  'LOW',    'IT_CORRIDOR',  58.0, 0.5),
('Perungudi',      13,  16.2, 4.8,  'LOW',    'IT_CORRIDOR',  62.0, 0.7),
('Madhavaram',     14,  20.1, 14.0, 'HIGH',   'RESIDENTIAL',  42.0, 4.0),
('Tondiarpet',     15,  13.5, 5.5,  'LOW',    'MIXED',        55.0, 0.4);

-- ============================================================
-- HISTORICAL FLOOD EVENTS — Ground Truth Records
-- ============================================================
INSERT INTO historical_floods (zone_id, event_date, event_name, flood_depth_cm, flood_duration_hours, rainfall_24h_cm, source) VALUES
(1,  '2015-12-01', '2015 Chennai Floods',      180, 72, 49.4, 'IMD / NDMA'),
(2,  '2015-12-01', '2015 Chennai Floods',      150, 60, 49.4, 'IMD / NDMA'),
(4,  '2015-12-01', '2015 Chennai Floods',      120, 48, 49.4, 'IMD / NDMA'),
(7,  '2015-12-01', '2015 Chennai Floods',      200, 72, 49.4, 'IMD / NDMA'),
(12, '2015-12-01', '2015 Chennai Floods',      160, 60, 49.4, 'IMD / NDMA'),
(13, '2015-12-01', '2015 Chennai Floods',      140, 48, 49.4, 'IMD / NDMA'),
(15, '2015-12-01', '2015 Chennai Floods',      170, 72, 49.4, 'IMD / NDMA'),
(1,  '2021-11-07', '2021 Chennai Floods',       90, 36, 21.0, 'IMD'),
(2,  '2021-11-07', '2021 Chennai Floods',      110, 48, 21.0, 'IMD'),
(7,  '2021-11-07', '2021 Chennai Floods',      130, 48, 21.0, 'IMD'),
(12, '2021-11-07', '2021 Chennai Floods',       85, 24, 21.0, 'IMD'),
(13, '2021-11-07', '2021 Chennai Floods',       95, 36, 21.0, 'IMD');
