from fastapi import FastAPI
from contextlib import asynccontextmanager

import asyncio

from app.infra.scripts import run_migrations, seed_data
from app.infra.settings.redis import init_redis, close_redis

from app.infra.settings.config import settings

from app.infra.api.routers.prices import router as prices_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(run_migrations)
    await seed_data()
    app.state.redis = await init_redis()
    yield
    await close_redis(app.state.redis)

app = FastAPI(app=settings.app_name, lifespan=lifespan)
app.include_router(prices_router, prefix="/prices", tags=["prices"])

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
