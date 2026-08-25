"""Parse database/seed_data.sql -- the source of truth for zone static
features -- instead of hardcoding a second copy that can drift out of sync.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

SEED_SQL_PATH = Path(__file__).resolve().parents[2] / "database" / "seed_data.sql"

# Matches one `INSERT INTO zones (...) VALUES (...)` statement. The
# ST_GeomFromText(...) call's WKT argument contains many literal ')'
# characters (the polygon ring), so it can't be skipped with a `[^)]*`
# class -- instead match non-greedily up to the ', 4326)' SRID argument,
# which is the one part of that call guaranteed not to contain ')'.
_ZONE_INSERT_RE = re.compile(
    r"INSERT INTO zones\b.*?VALUES\s*\(\s*"
    r"'(?P<zone_name>[^']+)'\s*,\s*"
    r"(?P<ward_number>\d+)\s*,\s*"
    r"ST_GeomFromText\(.*?,\s*4326\s*\)\s*,\s*"
    r"(?P<area_sqkm>[\d.]+)\s*,\s*"
    r"(?P<avg_elevation_m>[\d.]+)\s*,\s*"
    r"'(?P<drainage_capacity>[A-Z]+)'\s*,\s*"
    r"'(?P<land_use>[A-Z]+)'\s*,\s*"
    r"(?P<impervious_surface_pct>[\d.]+)\s*,\s*"
    r"(?P<proximity_to_water_km>[\d.]+)\s*\)\s*;",
    re.DOTALL,
)


def load_zone_static_features(seed_sql_path: Path = SEED_SQL_PATH) -> pd.DataFrame:
    """zone_id, zone_name, and the static terrain/drainage columns per zone.

    zone_id is assigned by insertion order (1-indexed), matching the SERIAL
    primary key zones.id gets when init.sql + seed_data.sql actually run,
    and matching the zone_id values used in historical_floods and
    config.FLOOD_EVENTS.
    """
    sql_text = seed_sql_path.read_text(encoding="utf-8")
    rows = []
    for i, m in enumerate(_ZONE_INSERT_RE.finditer(sql_text), start=1):
        rows.append(
            {
                "zone_id": i,
                "zone_name": m.group("zone_name"),
                "ward_number": int(m.group("ward_number")),
                "avg_elevation_m": float(m.group("avg_elevation_m")),
                "drainage_capacity": m.group("drainage_capacity"),
                "land_use": m.group("land_use"),
                "impervious_surface_pct": float(m.group("impervious_surface_pct")),
                "proximity_to_water_km": float(m.group("proximity_to_water_km")),
            }
        )

    if len(rows) != 15:
        raise ValueError(
            f"Expected 15 zone INSERT statements in {seed_sql_path}, parsed {len(rows)}. "
            "seed_data.sql may have changed shape -- update _ZONE_INSERT_RE."
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(load_zone_static_features().to_string(index=False))
