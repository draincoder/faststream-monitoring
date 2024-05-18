from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_telemetry(service_name: str, otlp_endpoint: str) -> TracerProvider:
    resource = Resource.create(attributes={"service.name": service_name})
    tracer_provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
    processor = BatchSpanProcessor(exporter)
    tracer_provider.add_span_processor(processor)
    trace.set_tracer_provider(tracer_provider)
    return tracer_provider
