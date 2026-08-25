"""Fetch and cache hourly Open-Meteo archive weather data, one call per zone
centroid (see config.ZONE_CENTROIDS for why -- a single shared coordinate
for every zone would erase the only signal rainfall can provide).
"""

from __future__ import annotations

import logging
import re
import time
from pathlib import Path

import pandas as pd
import requests

from ml_pipeline.pipeline.config import TIMEZONE, WEATHER_END, WEATHER_START, ZONE_CENTROIDS

logger = logging.getLogger(__name__)

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
HOURLY_VARS = "precipitation,relative_humidity_2m,temperature_2m"
REQUEST_TIMEOUT_S = 120
MAX_RETRIES = 5


def _slug(zone_name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", zone_name.lower()).strip("_")


def _cache_path(zone_name: str) -> Path:
    return DATA_DIR / f"raw_{_slug(zone_name)}.csv"


def fetch_zone_weather(
    zone_name: str, lat: float, lon: float, *, force: bool = False
) -> pd.DataFrame:
    """Hourly precipitation/humidity/temperature for one zone centroid.

    Cached to disk (ml_pipeline/data/, gitignored) so re-running feature
    engineering or retraining doesn't re-hit the API every time.
    """
    cache_path = _cache_path(zone_name)
    if cache_path.exists() and not force:
        logger.info("Using cached weather for %s (%s)", zone_name, cache_path.name)
        return pd.read_csv(cache_path, parse_dates=["time"])

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": WEATHER_START,
        "end_date": WEATHER_END,
        "hourly": HOURLY_VARS,
        "timezone": TIMEZONE,
    }
    logger.info("Fetching Open-Meteo archive for %s (%.4f, %.4f)", zone_name, lat, lon)
    resp = None
    for attempt in range(1, MAX_RETRIES + 1):
        resp = requests.get(ARCHIVE_URL, params=params, timeout=REQUEST_TIMEOUT_S)
        if resp.status_code != 429:
            break
        wait_s = 20 * attempt  # free tier rate limit -- back off and retry
        logger.warning(
            "429 rate-limited fetching %s, retry %d/%d in %ds",
            zone_name,
            attempt,
            MAX_RETRIES,
            wait_s,
        )
        time.sleep(wait_s)
    resp.raise_for_status()
    hourly = resp.json()["hourly"]

    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"])
    df.insert(0, "zone_name", zone_name)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(cache_path, index=False)
    return df


def fetch_all_zones(*, force: bool = False, sleep_s: float = 8.0) -> pd.DataFrame:
    """Fetch (or load cached) weather for every zone centroid, concatenated."""
    frames = []
    for zone_name, (lat, lon) in ZONE_CENTROIDS.items():
        already_cached = _cache_path(zone_name).exists() and not force
        frames.append(fetch_zone_weather(zone_name, lat, lon, force=force))
        if not already_cached:
            time.sleep(sleep_s)  # be polite to the free API on real requests
    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    combined = fetch_all_zones()
    print(combined.shape)
    print(combined.head())
