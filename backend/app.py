from fastapi import FastAPI

from app.infra.api.routers.prices import router as prices_router
from app.infra.api.routers.currency import router as currencies_router

app = FastAPI()
app.include_router(currencies_router, prefix="currencies")
app.include_router(prices_router, prefix="/prices")