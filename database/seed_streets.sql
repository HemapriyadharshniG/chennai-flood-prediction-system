-- seed_streets.sql
-- Description: PostGIS spatial seed data for Chennai street line geometries.
-- Contains representative streets across 15 zones, including known flood-prone underpasses.
-- SRID: 4326 (WGS84). Coordinate format: Longitude Latitude.

INSERT INTO streets (street_name, zone_id, geometry, is_underpass, elevation_m) VALUES
-- Zone 1: Adyar
('Adyar Bridge Road', 1, ST_GeomFromText('LINESTRING(80.252 13.010, 80.255 13.012, 80.258 13.015)', 4326), FALSE, 8.5),
('LB Road', 1, ST_GeomFromText('LINESTRING(80.255 12.990, 80.254 13.000, 80.252 13.008)', 4326), FALSE, 9.0),
('Sardar Patel Road', 1, ST_GeomFromText('LINESTRING(80.245 13.008, 80.250 13.009, 80.255 13.010)', 4326), FALSE, 10.2),
('Gandhi Nagar 1st Main Road', 1, ST_GeomFromText('LINESTRING(80.250 13.012, 80.252 13.014, 80.254 13.016)', 4326), FALSE, 9.5),

-- Zone 2: Velachery
('Velachery Main Road', 2, ST_GeomFromText('LINESTRING(80.215 12.975, 80.220 12.980, 80.225 12.985)', 4326), FALSE, 7.5),
('Taramani Link Road', 2, ST_GeomFromText('LINESTRING(80.225 12.985, 80.230 12.980, 80.235 12.978)', 4326), FALSE, 8.0),
('100 Feet Road Velachery', 2, ST_GeomFromText('LINESTRING(80.210 12.985, 80.215 12.982, 80.220 12.980)', 4326), FALSE, 8.2),
('Bypass Road Velachery', 2, ST_GeomFromText('LINESTRING(80.220 12.970, 80.225 12.972, 80.230 12.975)', 4326), FALSE, 7.8),

-- Zone 3: T. Nagar
('Usman Road', 3, ST_GeomFromText('LINESTRING(80.230 13.035, 80.232 13.040, 80.235 13.045)', 4326), FALSE, 11.5),
('Ranganathan Street', 3, ST_GeomFromText('LINESTRING(80.232 13.038, 80.234 13.039, 80.236 13.040)', 4326), FALSE, 11.0),
('South Usman Road', 3, ST_GeomFromText('LINESTRING(80.230 13.030, 80.232 13.033, 80.234 13.036)', 4326), FALSE, 10.8),
('GN Chetty Road', 3, ST_GeomFromText('LINESTRING(80.235 13.040, 80.240 13.045, 80.245 13.050)', 4326), FALSE, 12.0),
('Madley Subway', 3, ST_GeomFromText('LINESTRING(80.229 13.039, 80.230 13.040, 80.231 13.041)', 4326), TRUE, 5.5),

-- Zone 4: Mylapore
('Kutchery Road', 4, ST_GeomFromText('LINESTRING(80.265 13.032, 80.268 13.035, 80.270 13.038)', 4326), FALSE, 9.8),
('Luz Church Road', 4, ST_GeomFromText('LINESTRING(80.262 13.035, 80.265 13.035, 80.268 13.035)', 4326), FALSE, 10.0),
('Dr. Radhakrishnan Salai', 4, ST_GeomFromText('LINESTRING(80.260 13.040, 80.265 13.042, 80.270 13.045)', 4326), FALSE, 11.2),
('Mylapore Tank Street', 4, ST_GeomFromText('LINESTRING(80.268 13.033, 80.270 13.033, 80.272 13.034)', 4326), FALSE, 9.5),

-- Zone 5: Nungambakkam
('Nungambakkam High Road', 5, ST_GeomFromText('LINESTRING(80.240 13.055, 80.245 13.060, 80.250 13.065)', 4326), FALSE, 12.5),
('Khader Nawaz Khan Road', 5, ST_GeomFromText('LINESTRING(80.245 13.060, 80.247 13.062, 80.249 13.064)', 4326), FALSE, 13.0),
('Sterling Road', 5, ST_GeomFromText('LINESTRING(80.235 13.065, 80.240 13.065, 80.245 13.065)', 4326), FALSE, 12.2),
('Wallace Garden Road', 5, ST_GeomFromText('LINESTRING(80.248 13.062, 80.250 13.064, 80.252 13.066)', 4326), FALSE, 12.8),
('Kellys Subway', 5, ST_GeomFromText('LINESTRING(80.253 13.066, 80.254 13.067, 80.255 13.068)', 4326), TRUE, 6.0),

-- Zone 6: Anna Nagar
('2nd Avenue Anna Nagar', 6, ST_GeomFromText('LINESTRING(80.200 13.080, 80.205 13.085, 80.210 13.090)', 4326), FALSE, 14.5),
('3rd Avenue Anna Nagar', 6, ST_GeomFromText('LINESTRING(80.205 13.075, 80.210 13.080, 80.215 13.085)', 4326), FALSE, 14.2),
('Anna Nagar Roundtana Road', 6, ST_GeomFromText('LINESTRING(80.210 13.085, 80.212 13.087, 80.214 13.089)', 4326), FALSE, 14.8),
('Aminjikarai Subway', 6, ST_GeomFromText('LINESTRING(80.224 13.074, 80.225 13.075, 80.226 13.076)', 4326), TRUE, 7.0),

-- Zone 7: Porur
('Mount Poonamallee Road', 7, ST_GeomFromText('LINESTRING(80.140 13.020, 80.150 13.030, 80.160 13.040)', 4326), FALSE, 15.5),
('Porur Lake Road', 7, ST_GeomFromText('LINESTRING(80.150 13.035, 80.155 13.038, 80.160 13.042)', 4326), FALSE, 14.0),
('Arcot Road Porur', 7, ST_GeomFromText('LINESTRING(80.160 13.040, 80.165 13.045, 80.170 13.050)', 4326), FALSE, 16.0),

-- Zone 8: Tambaram
('GST Road Tambaram', 8, ST_GeomFromText('LINESTRING(80.110 12.910, 80.120 12.920, 80.130 12.930)', 4326), FALSE, 20.5),
('Tambaram Main Road', 8, ST_GeomFromText('LINESTRING(80.115 12.920, 80.125 12.925, 80.135 12.930)', 4326), FALSE, 19.8),
('Mudichur Road', 8, ST_GeomFromText('LINESTRING(80.110 12.915, 80.115 12.912, 80.120 12.910)', 4326), FALSE, 18.5),
('Tambaram Subway', 8, ST_GeomFromText('LINESTRING(80.127 12.924, 80.128 12.925, 80.129 12.926)', 4326), TRUE, 8.0),

-- Zone 9: Chromepet
('GST Road Chromepet', 9, ST_GeomFromText('LINESTRING(80.130 12.930, 80.140 12.940, 80.150 12.950)', 4326), FALSE, 22.0),
('Chromepet Radha Nagar Main Road', 9, ST_GeomFromText('LINESTRING(80.135 12.940, 80.140 12.945, 80.145 12.950)', 4326), FALSE, 21.5),
('Hasthinapuram Main Road', 9, ST_GeomFromText('LINESTRING(80.140 12.940, 80.145 12.942, 80.150 12.945)', 4326), FALSE, 21.0),

-- Zone 10: Guindy
('Mount Road Guindy', 10, ST_GeomFromText('LINESTRING(80.210 12.990, 80.215 13.000, 80.220 13.010)', 4326), FALSE, 12.0),
('Guindy Industrial Estate Road', 10, ST_GeomFromText('LINESTRING(80.215 13.005, 80.220 13.008, 80.225 13.010)', 4326), FALSE, 11.5),
('Sardar Patel Road Guindy', 10, ST_GeomFromText('LINESTRING(80.220 13.010, 80.225 13.012, 80.230 13.015)', 4326), FALSE, 11.8),

-- Zone 11: Kodambakkam
('Arcot Road Kodambakkam', 11, ST_GeomFromText('LINESTRING(80.210 13.045, 80.215 13.050, 80.220 13.055)', 4326), FALSE, 13.5),
('Kodambakkam High Road', 11, ST_GeomFromText('LINESTRING(80.220 13.050, 80.225 13.055, 80.230 13.060)', 4326), FALSE, 14.0),
('Duraiswamy Subway / Kodambakkam Subway', 11, ST_GeomFromText('LINESTRING(80.220 13.051, 80.221 13.052, 80.222 13.053)', 4326), TRUE, 5.0),
('Rangarajapuram Subway', 11, ST_GeomFromText('LINESTRING(80.217 13.054, 80.218 13.055, 80.219 13.056)', 4326), TRUE, 4.5),

-- Zone 12: Sholinganallur
('OMR Sholinganallur', 12, ST_GeomFromText('LINESTRING(80.220 12.890, 80.225 12.900, 80.230 12.910)', 4326), FALSE, 5.5),
('Sholinganallur Medavakkam Road', 12, ST_GeomFromText('LINESTRING(80.210 12.900, 80.215 12.902, 80.220 12.905)', 4326), FALSE, 6.0),
('Karapakkam Road', 12, ST_GeomFromText('LINESTRING(80.225 12.910, 80.230 12.915, 80.235 12.920)', 4326), FALSE, 5.2),
('ECR Link Road', 12, ST_GeomFromText('LINESTRING(80.230 12.900, 80.235 12.905, 80.240 12.910)', 4326), FALSE, 4.8),

-- Zone 13: Perungudi
('OMR Perungudi', 13, ST_GeomFromText('LINESTRING(80.230 12.950, 80.235 12.960, 80.240 12.970)', 4326), FALSE, 6.5),
('Perungudi Main Road', 13, ST_GeomFromText('LINESTRING(80.235 12.965, 80.240 12.965, 80.245 12.965)', 4326), FALSE, 6.2),
('Thoraipakkam Road', 13, ST_GeomFromText('LINESTRING(80.235 12.955, 80.240 12.952, 80.245 12.950)', 4326), FALSE, 6.0),

-- Zone 14: Madhavaram
('Madhavaram High Road', 14, ST_GeomFromText('LINESTRING(80.220 13.140, 80.225 13.145, 80.230 13.150)', 4326), FALSE, 12.0),
('Milk Colony Main Road', 14, ST_GeomFromText('LINESTRING(80.225 13.145, 80.230 13.150, 80.235 13.155)', 4326), FALSE, 11.5),
('GNT Road', 14, ST_GeomFromText('LINESTRING(80.220 13.150, 80.225 13.155, 80.230 13.160)', 4326), FALSE, 11.8),
('Perambur Subway', 14, ST_GeomFromText('LINESTRING(80.234 13.119, 80.235 13.120, 80.236 13.121)', 4326), TRUE, 5.5),

-- Zone 15: Tondiarpet
('TH Road Tondiarpet', 15, ST_GeomFromText('LINESTRING(80.270 13.110, 80.275 13.120, 80.280 13.130)', 4326), FALSE, 10.5),
('Tondiarpet High Road', 15, ST_GeomFromText('LINESTRING(80.275 13.125, 80.280 13.128, 80.285 13.130)', 4326), FALSE, 9.8),
('Old Washermanpet Road', 15, ST_GeomFromText('LINESTRING(80.280 13.120, 80.285 13.125, 80.290 13.130)', 4326), FALSE, 9.5),
('Vyasarpadi Subway', 15, ST_GeomFromText('LINESTRING(80.259 13.117, 80.260 13.118, 80.261 13.119)', 4326), TRUE, 3.8);
