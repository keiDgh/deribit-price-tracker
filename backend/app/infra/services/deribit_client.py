from app.infra.settings.config import settings

from app.application.exceptions import ExternalServiceBusinessError, ExternalServiceTransientError

import aiohttp
import asyncio
from decimal import Decimal

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

RETRYABLE_STATUS_CODES = frozenset({408, 429, 500, 502, 503, 504})

DEFAULT_TIMEOUT = aiohttp.ClientTimeout(
    total=30,
    connect=10,
    sock_read=15,
)

class DeribitClient:
    def __init__(self, session: aiohttp.ClientSession):
        self._session=session
        self._url=settings.deribit_api_url

    async def get_index_price(self, index_name: str) -> Decimal:
        result = await self._call(
            method="public/get_index_price",
            params={"index_name": index_name},
        )
        return Decimal(result["index_price"])

    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential_jitter(initial=0.5, max=10, jitter=0.3),
        retry=retry_if_exception_type(ExternalServiceTransientError),
        reraise=True,
    )
    async def _call(self, method: str, params: dict) -> dict:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }

        try:
            async with self._session.get(
                url=f"{self._url}/{method}",
                json=payload,
                timeout=DEFAULT_TIMEOUT,
            ) as response:
                
                if response.status in RETRYABLE_STATUS_CODES:
                    text = await response.text()
                    raise ExternalServiceTransientError(f"HTTP {response.status} from Deribit: {text}")

                if response.status >= 400:
                    text = await response.text()
                    raise ExternalServiceBusinessError(f"Deribit HTTP {response.status}: {text}")
                
                data = await response.json()

        except (
            aiohttp.ClientConnectionError,
            aiohttp.ServerTimeoutError,
            asyncio.TimeoutError,
        ) as e:
            raise ExternalServiceTransientError(f"Network error: {e}") from e

        if "error" in data:
            error = data["error"]
            raise ExternalServiceBusinessError(f"Deribit error {error.get('code')}: {error.get('message')}")
        
        return data["result"]