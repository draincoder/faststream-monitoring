from decimal import Decimal
from enum import Enum

from pydantic import BaseModel

from exchange.order_service.models import Order


class Status(Enum):
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"


class Trade(BaseModel):
    order: Order
    status: Status
    price: Decimal | None = None
