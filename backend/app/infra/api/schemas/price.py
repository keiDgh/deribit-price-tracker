from pydantic import BaseModel, ConfigDict

class PriceSchema(BaseModel):
    id: int
    ticker: str
    name: str
    price: float
    timestamp: int