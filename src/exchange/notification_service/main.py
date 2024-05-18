import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from faststream.rabbit.opentelemetry import RabbitTelemetryMiddleware

from exchange.common.config import load_config
from exchange.common.logging import configure_logging
from exchange.common.telemetry import setup_telemetry
from exchange.notification_service.handlers import router


async def main() -> None:
    configure_logging()
    config = load_config()
    tracer_provider = setup_telemetry(
        service_name="notification",
        otlp_endpoint=config.trace.otlp_endpoint,
    )
    telemetry_middleware = RabbitTelemetryMiddleware(tracer_provider=tracer_provider)
    broker = RabbitBroker(url=config.rabbit.url, middlewares=(telemetry_middleware,))
    broker.include_router(router)
    app = FastStream(broker)
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
