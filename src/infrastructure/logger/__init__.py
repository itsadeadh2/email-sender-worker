import logging


def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger
