from app.infra.settings.config import settings

from celery import Celery

celery_app = Celery(
    "deribit_index_price_service",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.infra.worker.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_accept_content=["json"],

    timezone="UTC",
    enable_utc=True,

    result_expires=3600,

    task_soft_time_limit=50,
    task_time_limit=60,

    beat_schedule={
        "collect-index-prices": {
            "task": "app.infra.worker.tasks.collect_index_price",
            "schedule": settings.collect_interval_seconds,
            "options": {"expires": 55},
        },
    },
    beat_schedule_filename="/tmp/celerybeat-schedule",
)