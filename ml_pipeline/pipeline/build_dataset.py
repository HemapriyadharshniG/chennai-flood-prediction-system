"""Build the model-ready dataset: per-zone weather + zone statics + rolling
rainfall windows + flood-event labels.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ml_pipeline.pipeline.config import DRAINAGE_SCORE_MAP, FLOOD_EVENTS
from ml_pipeline.pipeline.fetch_weather import fetch_all_zones
from ml_pipeline.pipeline.seed_zones import load_zone_static_features

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATASET_CACHE = DATA_DIR / "dataset_full.csv"

# Order matters -- this is exactly the order the model was trained on, and
# app/services/prediction_service.py must build its feature vector in this
# same order (it reads it back from model_metadata.json rather than
# hardcoding a second copy).
FEATURE_COLUMNS = [
    "rainfall_1h_cm",
    "rainfall_3h_cm",
    "rainfall_24h_cm",
    "rainfall_7d_cm",
    "humidity_pct",
    "temperature_c",
    "month",
    "is_monsoon",
    "avg_elevation_m",
    "drainage_capacity_score",
    "impervious_surface_pct",
    "proximity_to_water_km",
]


def _add_rolling_rainfall(df: pd.DataFrame) -> pd.DataFrame:
    """3h/24h/7d rolling sums of rainfall_1h_cm, grouped per zone.

    Grouping (rather than a global rolling window) keeps each zone's
    rolling sums from bleeding into the next zone's rows at the boundary
    between zones in the concatenated frame.
    """
    df = df.sort_values(["zone_name", "time"]).reset_index(drop=True)
    grouped = df.groupby("zone_name")["rainfall_1h_cm"]
    df["rainfall_3h_cm"] = grouped.transform(lambda s: s.rolling(3, min_periods=1).sum())
    df["rainfall_24h_cm"] = grouped.transform(lambda s: s.rolling(24, min_periods=1).sum())
    df["rainfall_7d_cm"] = grouped.transform(lambda s: s.rolling(24 * 7, min_periods=1).sum())
    return df


def _label_flooded(df: pd.DataFrame) -> pd.Series:
    """1 if (zone, timestamp) falls inside a known event window for that zone."""
    flooded = pd.Series(False, index=df.index)
    for zone_id, start, end in FLOOD_EVENTS:
        start_ts = pd.Timestamp(start)
        end_ts = pd.Timestamp(end) + pd.Timedelta(days=1)  # end date is inclusive
        mask = (df["zone_id"] == zone_id) & (df["time"] >= start_ts) & (df["time"] < end_ts)
        flooded |= mask
    return flooded.astype(int)


def build_dataset(*, force_refetch: bool = False, use_cache: bool = True) -> pd.DataFrame:
    """Weather (mm->cm, rolling windows) + zone statics + labels, one row per
    (zone, hour). Cached to disk since it's deterministic given the raw
    per-zone weather CSVs.
    """
    if use_cache and DATASET_CACHE.exists() and not force_refetch:
        return pd.read_csv(DATASET_CACHE, parse_dates=["time"])

    weather = fetch_all_zones(force=force_refetch)
    weather = weather.rename(
        columns={
            "precipitation": "rainfall_1h_cm",
            "relative_humidity_2m": "humidity_pct",
            "temperature_2m": "temperature_c",
        }
    )
    # Open-Meteo returns precipitation in mm; the schema (rainfall_readings,
    # flood_predictions) and the model both expect centimetres.
    weather["rainfall_1h_cm"] = weather["rainfall_1h_cm"] / 10.0

    zones = load_zone_static_features()
    df = weather.merge(zones, on="zone_name", how="inner")
    if df["zone_name"].nunique() != len(zones):
        missing = set(zones["zone_name"]) - set(df["zone_name"].unique())
        raise ValueError(f"Weather/zone merge dropped zones: {missing}")

    df = _add_rolling_rainfall(df)

    df["month"] = df["time"].dt.month
    df["is_monsoon"] = df["month"].isin([10, 11, 12]).astype(int)
    df["drainage_capacity_score"] = df["drainage_capacity"].map(DRAINAGE_SCORE_MAP)

    df["flooded"] = _label_flooded(df)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATASET_CACHE, index=False)
    return df


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    dataset = build_dataset()
    print(dataset.shape)
    print(dataset["flooded"].value_counts())
    print(dataset[FEATURE_COLUMNS + ["flooded"]].describe())
