-- Seed data for Chennai Flood Prediction System
-- Contains spatial geometries for Chennai zones and historical flood records

-- ==========================================
-- SECTION 1: CHENNAI ZONES
-- ==========================================

-- 1. Adyar
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Adyar', 1, ST_GeomFromText('POLYGON((80.2415 12.9862, 80.2715 12.9862, 80.2715 13.0162, 80.2415 13.0162, 80.2415 12.9862))', 4326), 12.5, 4.2, 'LOW', 'RESIDENTIAL', 72.0, 0.3);

-- 2. Velachery
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Velachery', 2, ST_GeomFromText('POLYGON((80.2000 12.9635, 80.2360 12.9635, 80.2360 12.9995, 80.2000 12.9995, 80.2000 12.9635))', 4326), 15.3, 5.8, 'LOW', 'RESIDENTIAL', 75.0, 0.1);

-- 3. T. Nagar
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('T. Nagar', 3, ST_GeomFromText('POLYGON((80.2201 13.0278, 80.2481 13.0278, 80.2481 13.0558, 80.2201 13.0558, 80.2201 13.0278))', 4326), 8.7, 8.5, 'MEDIUM', 'COMMERCIAL', 85.0, 1.2);

-- 4. Mylapore
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Mylapore', 4, ST_GeomFromText('POLYGON((80.2526 13.0189, 80.2826 13.0189, 80.2826 13.0489, 80.2526 13.0489, 80.2526 13.0189))', 4326), 10.2, 6.3, 'MEDIUM', 'RESIDENTIAL', 80.0, 0.5);

-- 5. Nungambakkam
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Nungambakkam', 5, ST_GeomFromText('POLYGON((80.2295 13.0439, 80.2555 13.0439, 80.2555 13.0699, 80.2295 13.0699, 80.2295 13.0439))', 4326), 7.8, 9.1, 'MEDIUM', 'COMMERCIAL', 82.0, 0.8);

-- 6. Anna Nagar
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Anna Nagar', 6, ST_GeomFromText('POLYGON((80.1930 13.0680, 80.2270 13.0680, 80.2270 13.1020, 80.1930 13.1020, 80.1930 13.0680))', 4326), 14.1, 11.2, 'HIGH', 'RESIDENTIAL', 70.0, 1.5);

-- 7. Porur
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Porur', 7, ST_GeomFromText('POLYGON((80.1368 13.0155, 80.1768 13.0155, 80.1768 13.0555, 80.1368 13.0555, 80.1368 13.0155))', 4326), 18.4, 6.0, 'LOW', 'MIXED', 65.0, 0.2);

-- 8. Tambaram
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Tambaram', 8, ST_GeomFromText('POLYGON((80.1048 12.9019, 80.1508 12.9019, 80.1508 12.9479, 80.1048 12.9479, 80.1048 12.9019))', 4326), 22.6, 12.5, 'MEDIUM', 'RESIDENTIAL', 60.0, 1.0);

-- 9. Chromepet
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Chromepet', 9, ST_GeomFromText('POLYGON((80.1284 12.9356, 80.1604 12.9356, 80.1604 12.9676, 80.1284 12.9676, 80.1284 12.9356))', 4326), 11.3, 10.8, 'MEDIUM', 'RESIDENTIAL', 62.0, 1.2);

-- 10. Guindy
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Guindy', 10, ST_GeomFromText('POLYGON((80.2066 12.9927, 80.2346 12.9927, 80.2346 13.0207, 80.2066 13.0207, 80.2066 12.9927))', 4326), 9.5, 7.5, 'MEDIUM', 'INDUSTRIAL', 78.0, 0.6);

-- 11. Kodambakkam
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Kodambakkam', 11, ST_GeomFromText('POLYGON((80.2120 13.0402, 80.2360 13.0402, 80.2360 13.0642, 80.2120 13.0642, 80.2120 13.0402))', 4326), 6.8, 8.0, 'MEDIUM', 'RESIDENTIAL', 80.0, 1.1);

-- 12. Sholinganallur
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Sholinganallur', 12, ST_GeomFromText('POLYGON((80.2039 12.8770, 80.2519 12.8770, 80.2519 12.9250, 80.2039 12.9250, 80.2039 12.8770))', 4326), 25.7, 3.5, 'LOW', 'COMMERCIAL', 65.0, 0.4);

-- 13. Perungudi
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Perungudi', 13, ST_GeomFromText('POLYGON((80.2235 12.9441, 80.2615 12.9441, 80.2615 12.9821, 80.2235 12.9821, 80.2235 12.9441))', 4326), 16.2, 4.8, 'LOW', 'COMMERCIAL', 70.0, 0.3);

-- 14. Madhavaram
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Madhavaram', 14, ST_GeomFromText('POLYGON((80.2108 13.1276, 80.2528 13.1276, 80.2528 13.1696, 80.2108 13.1696, 80.2108 13.1276))', 4326), 20.1, 14.0, 'HIGH', 'MIXED', 55.0, 2.0);

-- 15. Tondiarpet
INSERT INTO zones (zone_name, ward_number, geometry, area_sqkm, avg_elevation_m, drainage_capacity, land_use, impervious_surface_pct, proximity_to_water_km)
VALUES ('Tondiarpet', 15, ST_GeomFromText('POLYGON((80.2686 13.1086, 80.3026 13.1086, 80.3026 13.1426, 80.2686 13.1426, 80.2686 13.1086))', 4326), 13.5, 5.5, 'LOW', 'MIXED', 76.0, 0.1);


-- ==========================================
-- SECTION 2: HISTORICAL FLOODS
-- ==========================================

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
