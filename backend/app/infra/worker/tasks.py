from app.infra.worker.runtime import load_currency_ids
from app.infra.services import DeribitClient
from app.infra.repositories import SqlPriceRepository
from app.infra.db.session import get_async_session

from app.domain.exceptions import DuplicatePriceError, RelatedCurrencyNotFound

import aiohttp
import asyncio
import time

from celery import shared_task

async def _collect_index_prices() -> None:
    currency_ids = await load_currency_ids()

    async with aiohttp.ClientSession() as http_session:
        client = DeribitClient(http_session)

        btc_price = await client.get_index_price("btc_usd")
        eth_price = await client.get_index_price("eth_usd")

    now = int(time.time())

    async with get_async_session() as db_session:
        repo = SqlPriceRepository(db_session)

        try:
            await repo.add(
                currency_id=currency_ids["btc_usd"],
                price=btc_price,
                timestamp=now,
            )
            await repo.add(
                currency_id=currency_ids["eth_usd"],
                price=eth_price,
                timestamp=now,
            )
        except DuplicatePriceError:
            pass
        except RelatedCurrencyNotFound:
            raise

@shared_task(name="app.infra.worker.tasks.collect_index_price")
def collect_index_price():
    asyncio.run(_collect_index_prices())