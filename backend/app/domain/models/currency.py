from dataclasses import dataclass

@dataclass
class Currency:
    id: int
    ticker: str
    name: str