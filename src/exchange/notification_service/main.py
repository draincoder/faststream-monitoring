import uvicorn
from faststream.asgi import AsgiFastStream
from faststream.rabbit import RabbitBroker
from faststream.rabbit.opentelemetry import RabbitTelemetryMiddleware
from faststream.rabbit.prometheus import RabbitPrometheusMiddleware
from prometheus_client import CollectorRegistry, make_asgi_app

from exchange.common.config import load_config
from exchange.common.logging import configure_logging
from exchange.common.telemetry import setup_telemetry
from exchange.notification_service.handlers import router


def main() -> AsgiFastStream:
    configure_logging()
    config = load_config()
    service_name = "notification"
    tracer_provider = setup_telemetry(
        service_name=service_name,
        otlp_endpoint=config.trace.otlp_endpoint,
    )
    registry = CollectorRegistry()

    telemetry_middleware = RabbitTelemetryMiddleware(tracer_provider=tracer_provider)
    prometheus_middleware = RabbitPrometheusMiddleware(
        registry=registry,
        app_name=service_name,
        metrics_prefix="faststream",
    )
    broker = RabbitBroker(url=config.rabbit.url, middlewares=(telemetry_middleware, prometheus_middleware))
    broker.include_router(router)
    return AsgiFastStream(broker, [("/metrics", make_asgi_app(registry))])


if __name__ == "__main__":
    uvicorn.run(main(), host="0.0.0.0", port=8080)
