from pydantic import BaseModel, ConfigDict

class PriceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticker: str
    name: str
    price: float
    timestamp: int