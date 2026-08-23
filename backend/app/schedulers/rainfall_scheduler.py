"""Background job scheduler for telemetry ingestion and periodic batch predictions."""

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

# TODO: Define and register periodic tasks:
# 1. Fetch live rainfall telemetry every 30 minutes:
#    @scheduler.scheduled_job("interval", minutes=30)
#    async def fetch_live_rainfall_job(): ...
#
# 2. Re-run batch predictions across all Chennai zones every 1 hour:
#    @scheduler.scheduled_job("interval", hours=1)
#    async def rerun_batch_predictions_job(): ...
#
# 3. Check threshold-based flood alerts every 15 minutes:
#    @scheduler.scheduled_job("interval", minutes=15)
#    async def check_flood_alerts_job(): ...


def start_rainfall_scheduler():
    """Start APScheduler background runner."""
    # TODO: scheduler.start()
    pass
