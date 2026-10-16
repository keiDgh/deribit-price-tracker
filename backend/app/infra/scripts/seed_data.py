from app.infra.repositories import SqlCurrencyRepository
from app.infra.db.session import get_async_session

INITIAL_CURRENCIES = (
    ("btc_usd", "Bitcoin"),
    ("eth_usd", "Ethereum"),
)

async def seed_data():
    async with get_async_session() as session:
        currency_repository = SqlCurrencyRepository(session)

        for ticker, name in INITIAL_CURRENCIES:
            existing = await currency_repository.get_by_ticker(ticker)
            if existing is None:
                await currency_repository.add(ticker=ticker, name=name)
