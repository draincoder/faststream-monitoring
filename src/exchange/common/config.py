import os
import tomllib
from dataclasses import dataclass
from typing import Any, cast

from adaptix import Retort

DEFAULT_CONFIG_PATH = "./config/config.toml"


@dataclass
class RabbitConfig:
    user: str
    password: str
    port: int = 5672
    host: str = "localhost"

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"


@dataclass
class TraceConfig:
    otlp_endpoint: str


@dataclass
class Config:
    rabbit: RabbitConfig
    trace: TraceConfig


def read_toml(path: str) -> dict[str, Any]:
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_config() -> Config:
    path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)
    data = read_toml(path)
    mapper = Retort()
    return cast("Config", mapper.load(data, Config))
