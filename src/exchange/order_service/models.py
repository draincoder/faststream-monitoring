from enum import Enum

from pydantic import BaseModel


class Direction(Enum):
    BUY = "BUY"
    SELL = "SELL"


class Order(BaseModel):
    symbol: str
    quantity: int
    type: Direction
