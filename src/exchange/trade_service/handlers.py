import asyncio
import logging
import random
from decimal import Decimal

from faststream.rabbit import RabbitRouter
from opentelemetry import trace

from exchange.trade_service.models import Status, Trade

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
router = RabbitRouter()


@router.publisher("notifications")
@router.subscriber("trades")
async def trades_handler(trade: Trade) -> str:
    logging.info("Received trade [%s]", trade)

    with tracer.start_as_current_span("process trade"):
        price = Decimal(random.randint(1000, 1500))
        trade.price = price
        trade.status = Status.SUBMITTED
        await asyncio.sleep(random.randint(1, 50) / 10)

    message = f"Order [{trade.order}] was executed at the asset price {trade.price}$"
    logging.info(message)

    return message
