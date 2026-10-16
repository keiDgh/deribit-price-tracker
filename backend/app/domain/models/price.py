from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Price:
    id: int
    currency_id: int
    price: Decimal
    timestamp: int
    created_at: datetime