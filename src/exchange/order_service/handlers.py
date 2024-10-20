import asyncio
import logging
import random

from faststream.rabbit import RabbitRouter
from opentelemetry import trace

from exchange.order_service.models import Order
from exchange.trade_service.models import Status, Trade

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
router = RabbitRouter()


@router.publisher("trades")
@router.subscriber("orders")
async def orders_handler(order: Order) -> Trade:
    logging.info("Received order [%s]", order)

    with tracer.start_as_current_span("validate order", attributes={"quantity": order.quantity}):
        await asyncio.sleep(random.randint(1, 50) / 10)
        if order.quantity <= 0:
            raise ValueError("Order quantity must be greater than zero")

    return Trade(order=order, status=Status.PENDING)
