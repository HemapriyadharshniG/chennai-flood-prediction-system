"""Static configuration for the training pipeline: zone centroids, known flood
event windows used as labels, and the risk-band thresholds the backend
inference path (`app/ml/model_loader.py`) is expected to use.
"""

WEATHER_START = "2014-01-01"
WEATHER_END = "2024-12-31"
TIMEZONE = "Asia/Kolkata"

# One centroid per zone -- Open-Meteo is queried once per zone, not once for
# the whole city. A single shared coordinate would give every zone identical
# rainfall at every timestamp, leaving static terrain as the only thing that
# distinguishes zones, and the model would degenerate into memorising which
# zones appear in FLOOD_EVENTS rather than learning from rainfall.
ZONE_CENTROIDS = {
    "Adyar": (13.0012, 80.2565),
    "Velachery": (12.9815, 80.2180),
    "T. Nagar": (13.0418, 80.2341),
    "Mylapore": (13.0339, 80.2676),
    "Nungambakkam": (13.0569, 80.2425),
    "Anna Nagar": (13.0850, 80.2100),
    "Porur": (13.0355, 80.1568),
    "Tambaram": (12.9249, 80.1278),
    "Chromepet": (12.9516, 80.1444),
    "Guindy": (13.0067, 80.2206),
    "Kodambakkam": (13.0522, 80.2240),
    "Sholinganallur": (12.9010, 80.2279),
    "Perungudi": (12.9631, 80.2425),
    "Madhavaram": (13.1486, 80.2318),
    "Tondiarpet": (13.1256, 80.2856),
}

# (zone_id, start_date, end_date) inclusive. zone_id matches the 1-indexed
# insertion order in database/seed_data.sql, which is also the order
# database/init.sql's SERIAL zones.id would assign, and matches the zone_id
# values already used in the historical_floods seed rows.
#
# Only three events across eleven years of hourly data, and each is a
# zone-level "these wards flooded" list rather than a per-timestamp
# measurement. That is a very small, coarse set of positive labels -- see
# the README caveat before treating this model as more than a demonstrator.
FLOOD_EVENTS = [
    # 2015-11-30 .. 2015-12-03: 2015 Chennai floods
    (1, "2015-11-30", "2015-12-03"),
    (2, "2015-11-30", "2015-12-03"),
    (4, "2015-11-30", "2015-12-03"),
    (7, "2015-11-30", "2015-12-03"),
    (12, "2015-11-30", "2015-12-03"),
    (13, "2015-11-30", "2015-12-03"),
    (15, "2015-11-30", "2015-12-03"),
    # 2021-11-07 .. 2021-11-11: 2021 Chennai floods
    (1, "2021-11-07", "2021-11-11"),
    (2, "2021-11-07", "2021-11-11"),
    (7, "2021-11-07", "2021-11-11"),
    (12, "2021-11-07", "2021-11-11"),
    (13, "2021-11-07", "2021-11-11"),
    # Cyclone Michaung. The brief specified 2023-12-17..2023-12-20, but the
    # actual Open-Meteo archive rainfall for Chennai shows essentially zero
    # precipitation in that window and a sharp, well-documented spike on
    # 2023-12-04 (23.5cm/24h at the Adyar centroid) -- matching Michaung's
    # real Chennai landfall date. Corrected here; see ml_pipeline/README.md.
    (1, "2023-12-03", "2023-12-05"),
    (2, "2023-12-03", "2023-12-05"),
    (12, "2023-12-03", "2023-12-05"),
    (13, "2023-12-03", "2023-12-05"),
]

# zones.drainage_capacity is categorical ('LOW'/'MEDIUM'/'HIGH') -- the model
# needs a numeric feature, so this is the fixed mapping both the training
# pipeline and backend/app/services/prediction_service.py must use.
DRAINAGE_SCORE_MAP = {"LOW": 0.2, "MEDIUM": 0.5, "HIGH": 0.8}

# Upper bound (inclusive) of flood_probability for each band.
RISK_THRESHOLDS = {"LOW": 0.25, "MODERATE": 0.55, "HIGH": 0.80, "CRITICAL": 1.0}

# Chronological split, not a random one: a random split would leak future
# rainfall into training through the rolling windows. Everything from this
# date onward is test data, which holds out the entire Dec 2023 event.
TRAIN_TEST_SPLIT_DATE = "2023-10-01"
