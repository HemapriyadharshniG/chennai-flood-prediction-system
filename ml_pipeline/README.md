# ML Training Pipeline

Trains the LightGBM flood-risk classifier used by `backend/app/ml/`. Plain,
rerunnable `.py` modules under `pipeline/` rather than a notebook, so the
pipeline diffs cleanly and can be re-run end to end without a Jupyter
kernel. Runs entirely on CPU, on Windows, with no `geopandas`/`rasterio` —
elevation and drainage are already available per zone in
`database/seed_data.sql`, so nothing in this pipeline needs to touch a
raster or reproject a shapefile.

## Setup

```
python -m venv .venv
.venv\Scripts\activate
pip install -r ml_pipeline\requirements.txt
```

## Run

From the repo root:

```
python -m ml_pipeline.pipeline.train
```

This will, in order:

1. **Fetch weather** (`pipeline/fetch_weather.py`) — one Open-Meteo archive
   API call per zone centroid (15 calls, `2014-01-01` to `2024-12-31`,
   hourly precipitation / humidity / temperature, `Asia/Kolkata`). Each
   zone's raw response is cached to `ml_pipeline/data/raw_<zone>.csv`, so a
   second run doesn't re-fetch anything. The free API tier rate-limits
   aggressively (HTTP 429) if all 15 calls fire back-to-back; the fetcher
   retries with backoff and paces requests, but a full cold fetch can take
   several minutes.
2. **Build the dataset** (`pipeline/build_dataset.py`) — merges weather with
   each zone's static features (parsed straight out of
   `database/seed_data.sql`, not hardcoded, so the two can't drift apart),
   converts precipitation from Open-Meteo's mm to the schema's cm, computes
   3h/24h/7d rolling rainfall sums *grouped per zone*, and derives `month`
   / `is_monsoon` (Oct-Dec). Cached to `ml_pipeline/data/dataset_full.csv`.
3. **Label** — `flooded=1` for any `(zone, hour)` inside a known flood
   event's window for that zone, else `0`. Event windows are in
   `pipeline/config.py::FLOOD_EVENTS`.
4. **Train** (`pipeline/train.py`) — `LGBMClassifier`,
   `class_weight="balanced"` (floods are rare), early stopping. The split
   is **chronological**, not random: everything before
   `config.TRAIN_TEST_SPLIT_DATE` (2023-10-01) is training data, everything
   from that date on is the test set — which holds out the entire Dec 2023
   event. A random/stratified split would leak future rainfall into
   training through the rolling windows and inflate every metric.
5. **Export** — `joblib.dump`s the model to
   `ml_pipeline/models/lightgbm_flood_model.pkl` and writes
   `ml_pipeline/models/model_metadata.json` (feature column order, risk
   thresholds, sample counts, precision/recall/ROC-AUC). Both are
   gitignored in this pipeline dir; a separate branch/PR copies them into
   `backend/app/ml/` for the API to load.

To force a clean refetch/rebuild instead of using the cache:

```python
from ml_pipeline.pipeline.train import train
train(force_refetch=True)
```

## Honest caveats on label quality

The positive labels come from **three** documented flood events across
eleven years (2015, 2021, 2023), and each is a *zone-level* "these wards
flooded" list, not a per-timestamp measurement of actual water depth at
each hour. That is a very small, coarse set of positive examples for a
binary classifier trained on ~1.4M hourly rows — 1,272 positive training
rows and 288 positive test rows out of 1.45M total, all clustered into a
handful of multi-day windows.

Two concrete problems surfaced while building this, worth knowing before
trusting the numbers:

1. **The 2023 event date in the original brief was wrong.** It specified
   2023-12-17..2023-12-20 for Cyclone Michaung, but the fetched Open-Meteo
   archive shows essentially zero rainfall in that window and a sharp,
   well-documented spike on **2023-12-04** (23.5cm/24h at the Adyar
   centroid) — matching Michaung's actual Chennai landfall. `config.py` now
   uses `2023-12-03..2023-12-05`. Before this fix, the held-out test set
   (everything from `TRAIN_TEST_SPLIT_DATE` onward, which is where this
   event lands) had *no* rainfall signal for its positive class at all, and
   the model scored ROC-AUC ≈ 0.50 — indistinguishable from random. After
   the fix: precision 0.156, recall 0.774, ROC-AUC 0.993.
2. **The 2015 event is real but understated by the data source.** Dec 1,
   2015 — the day of the actual record-breaking rainfall — falls correctly
   inside the given window, but Open-Meteo's archive (ERA5-family
   reanalysis, ~25km grid) shows only ~4.9cm that day at Adyar, versus the
   ~49cm actually recorded in Chennai. Reanalysis products are known to
   smooth out extreme localised/convective rainfall; there's no date fix
   for this one, it's an inherent limitation of using free reanalysis data
   in place of ground station or radar observations. The 2015 event still
   contributes positive labels and some training signal, just weaker than
   the real event warranted.

So: precision/recall/ROC-AUC on the held-out Dec 2023 event tell you
whether the model recognises rainfall/terrain patterns similar to the known
events in *this particular weather dataset* — not whether it would
correctly flag a genuinely novel flood scenario, and not whether "flooded"
is the right label for every hour inside a multi-day event window (a zone
doesn't stay underwater for all 48-72 hours of one). Treat this model as a
**demonstrator** of the pipeline end-to-end (fetch -> feature engineer ->
train -> export -> serve), not a validated flood predictor. Report
precision/recall/ROC-AUC, never a bare accuracy number — with this class
imbalance, a model that never predicts a flood scores well over 99.8%
accuracy while being useless.
