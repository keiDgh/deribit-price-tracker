from app.infra.db.session import get_async_session
from app.infra.repositories import SqlCurrencyRepository

async def load_currency_ids() -> dict[str, int]:
    currency_ids = {}

    async with get_async_session() as session:

        repository = SqlCurrencyRepository(session)
        for ticker in ("btc_usd", "eth_usd"):
            currency = await repository.get_by_ticker(ticker)
            if currency is None:
                raise RuntimeError(f"Currency {ticker} not seeded")
            currency_ids[ticker] = currency.id

    return currency_ids