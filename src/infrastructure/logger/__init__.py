import logging
from logging import StreamHandler


def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger
