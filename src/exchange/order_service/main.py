import asyncio
import random

import uvicorn
from faststream.asgi import AsgiFastStream
from faststream.rabbit import RabbitBroker
from faststream.rabbit.opentelemetry import RabbitTelemetryMiddleware
from faststream.rabbit.prometheus import RabbitPrometheusMiddleware
from prometheus_client import CollectorRegistry, make_asgi_app

from exchange.common.config import load_config
from exchange.common.logging import configure_logging
from exchange.common.telemetry import setup_telemetry
from exchange.order_service.handlers import router
from exchange.order_service.models import Direction, Order


def main() -> AsgiFastStream:
    configure_logging()
    config = load_config()
    service_name = "order"
    tracer_provider = setup_telemetry(
        service_name=service_name,
        otlp_endpoint=config.trace.otlp_endpoint,
    )
    registry = CollectorRegistry()

    telemetry_middleware = RabbitTelemetryMiddleware(tracer_provider=tracer_provider)
    prometheus_middleware = RabbitPrometheusMiddleware(
        registry=registry, app_name=service_name, metrics_prefix="faststream"
    )
    broker = RabbitBroker(url=config.rabbit.url, middlewares=(telemetry_middleware, prometheus_middleware))
    broker.include_router(router)
    app = AsgiFastStream(broker, [("/metrics", make_asgi_app(registry))])

    @app.after_startup
    async def after_startup() -> None:
        while True:
            await broker.publish(Order(symbol="AAPL", quantity=10, type=Direction.BUY), "orders")
            await broker.publish(Order(symbol="AAPL" * 100, quantity=5, type=Direction.BUY), "orders")
            await broker.publish(Order(symbol="AAPL" * 300, quantity=1, type=Direction.BUY), "orders")
            await broker.publish(Order(symbol="AAPL", quantity=-1, type=Direction.BUY), "orders")
            await asyncio.sleep(random.randint(1, 50) / 10)

    return app


if __name__ == "__main__":
    uvicorn.run(main(), host="0.0.0.0", port=8080)
