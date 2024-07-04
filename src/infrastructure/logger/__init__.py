import logging
from logging import StreamHandler


def create_logger():
    log_format = '%(levelname)s - %(message)s'

    # Create a RotatingFileHandler to manage log file size
    handler = StreamHandler()

    # Create a formatter and set it for the handler
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    # Add the handler to the Flask app's logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger

