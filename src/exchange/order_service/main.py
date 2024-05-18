import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from faststream.rabbit.opentelemetry import RabbitTelemetryMiddleware

from exchange.common.config import load_config
from exchange.common.logging import configure_logging
from exchange.common.telemetry import setup_telemetry
from exchange.order_service.handlers import router
from exchange.order_service.models import Direction, Order


async def main() -> None:
    configure_logging()
    config = load_config()
    tracer_provider = setup_telemetry(
        service_name="order",
        otlp_endpoint=config.trace.otlp_endpoint,
    )
    telemetry_middleware = RabbitTelemetryMiddleware(tracer_provider=tracer_provider)
    broker = RabbitBroker(url=config.rabbit.url, middlewares=(telemetry_middleware,))
    broker.include_router(router)
    app = FastStream(broker)

    @app.after_startup
    async def after_startup() -> None:
        await broker.publish(Order(symbol="AAPL", quantity=10, type=Direction.BUY), "orders")
        await broker.publish(Order(symbol="AAPL", quantity=5, type=Direction.BUY), "orders")
        await broker.publish(Order(symbol="AAPL", quantity=1, type=Direction.BUY), "orders")

    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
