from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class PriceSchema(BaseModel):
    id: int
    ticker: str
    name: str
    price: Decimal
    timestamp: int