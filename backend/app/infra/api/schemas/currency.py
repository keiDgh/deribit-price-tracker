from pydantic import BaseModel, ConfigDict

class CurrencySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    ticker: str
    name: str