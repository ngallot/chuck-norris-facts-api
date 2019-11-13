import logging
from app.config import LoggingConfig


def build_logger(logger_name: str, config: LoggingConfig) -> logging.Logger:
    logging.basicConfig(level=config.level, format=config.format)
    return logging.getLogger(name=logger_name)
