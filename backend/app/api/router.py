"""Aggregates all endpoint routers under a single top-level router.

Endpoint modules own only their relative paths (e.g. `/zones`); the `/api`
prefix is applied once, where this router is included in main.py.
"""

from fastapi import APIRouter

from app.api.endpoints import history, predictions, rainfall, streets, zones

router = APIRouter()

router.include_router(zones.router)
router.include_router(predictions.router)
router.include_router(rainfall.router)
router.include_router(streets.router)
router.include_router(history.router)
