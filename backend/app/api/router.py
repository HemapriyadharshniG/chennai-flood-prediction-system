"""Main API router combining all endpoint modules."""

from fastapi import APIRouter

router = APIRouter(prefix="/api")

# TODO: Include endpoint routers when implemented:
# - zones: router.include_router(zones.router, prefix="/zones", tags=["Zones"])
# - rainfall: router.include_router(rainfall.router, prefix="/rainfall", tags=["Rainfall"])
# - predictions: router.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
# - history: router.include_router(history.router, prefix="/history", tags=["History"])
# - streets: router.include_router(streets.router, prefix="/streets", tags=["Streets"])
