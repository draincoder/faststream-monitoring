import logging


def configure_logging() -> None:
    fmt_str = "[%(asctime)s] - %(levelname)s - [%(module)s:%(lineno)s:%(funcName)s] - %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt_str)
