import asyncio
import logging
import random

from faststream.rabbit import RabbitRouter
from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
router = RabbitRouter()


async def send_notification(text: str) -> None:
    with tracer.start_as_current_span("send notification", attributes={"text": text}):
        await asyncio.sleep(random.randint(1, 50) / 10)

    logger.info("Notification sent successfully")


@router.subscriber("notifications")
async def notifications_handler(message: str) -> None:
    logger.info("Received message [%s]", message)
    await send_notification(message)
