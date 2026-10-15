from dataclasses import dataclass
from datetime import datetime

@dataclass
class Price:
    id: int
    currency_id: int
    price: float
    timestamp: int
    created_at: datetime