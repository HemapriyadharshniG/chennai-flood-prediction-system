"""Train the LightGBM flood-risk classifier and export the model artifact.

Chronological split, not sklearn's train_test_split with stratify: a random
split would leak future rainfall into the training set through the rolling
windows (a 7-day window ending just before a test-set timestamp can share
hours with a training-set row a few hours away), inflating the reported
metrics. Instead everything before TRAIN_TEST_SPLIT_DATE is training data
and everything from that date on is test data, which holds out the most
recent known event (Dec 2023) entirely.

CAVEAT: only three flood events across eleven years back the positive
labels, and each is a zone-level "these wards flooded" list rather than a
per-timestamp measurement. That is a very small, coarse label set -- this
model is a demonstrator, not a validated flood predictor. See ml_pipeline's
README for the full caveat.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import joblib
import lightgbm as lgb
import pandas as pd
from sklearn.metrics import precision_score, recall_score, roc_auc_score

from ml_pipeline.pipeline.build_dataset import FEATURE_COLUMNS, build_dataset
from ml_pipeline.pipeline.config import RISK_THRESHOLDS, TRAIN_TEST_SPLIT_DATE

logger = logging.getLogger(__name__)

MODEL_DIR = Path(__file__).resolve().parents[1] / "models"
MODEL_PATH = MODEL_DIR / "lightgbm_flood_model.pkl"
METADATA_PATH = MODEL_DIR / "model_metadata.json"


def train(*, force_refetch: bool = False) -> dict:
    df = build_dataset(force_refetch=force_refetch)

    split_ts = pd.Timestamp(TRAIN_TEST_SPLIT_DATE)
    train_df = df[df["time"] < split_ts]
    test_df = df[df["time"] >= split_ts]

    X_train, y_train = train_df[FEATURE_COLUMNS], train_df["flooded"]
    X_test, y_test = test_df[FEATURE_COLUMNS], test_df["flooded"]

    logger.info(
        "train=%d rows (%d positive) | test=%d rows (%d positive)",
        len(X_train),
        int(y_train.sum()),
        len(X_test),
        int(y_test.sum()),
    )

    model = lgb.LGBMClassifier(
        objective="binary",
        class_weight="balanced",  # floods are rare; unweighted would just predict 0 everywhere
        n_estimators=500,
        learning_rate=0.05,
        num_leaves=31,
        random_state=42,
    )
    model.fit(
        X_train,
        y_train,
        eval_set=[(X_test, y_test)],
        eval_metric="auc",
        callbacks=[lgb.early_stopping(stopping_rounds=30, verbose=False)],
    )

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    roc_auc = float(roc_auc_score(y_test, y_proba)) if y_test.nunique() > 1 else None
    metrics = {
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "roc_auc": roc_auc,
    }

    # Accuracy is meaningless here -- with floods this rare, "predict 0
    # always" scores well over 99% accuracy while catching nothing.
    logger.info("Test metrics (precision/recall/ROC-AUC): %s", metrics)
    logger.warning(
        "Only 3 flood events across 11 years back these labels, and they are "
        "zone-level event windows, not per-timestamp ground truth. Treat this "
        "model as a demonstrator, not a validated predictor."
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    metadata = {
        "feature_columns": FEATURE_COLUMNS,
        "model_type": "LGBMClassifier",
        "risk_thresholds": RISK_THRESHOLDS,
        "training_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "roc_auc": metrics["roc_auc"],
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "train_test_split_date": TRAIN_TEST_SPLIT_DATE,
        "caveat": (
            "Trained on only 3 known flood events across 2014-2024, labelled "
            "as zone-level event windows rather than per-timestamp ground "
            "truth. This is a demonstrator model, not a validated predictor."
        ),
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    logger.info("Wrote %s and %s", MODEL_PATH, METADATA_PATH)

    return metrics


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train()
