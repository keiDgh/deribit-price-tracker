from dataclasses import dataclass
from datetime import datetime

@dataclass
class Price:
    id: int
    currency_id: int
    price_usd: str
    created_at: datetime