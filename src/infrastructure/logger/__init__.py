import logging
from logging import StreamHandler


def create_logger():
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Get the root logger
    logger = logging.getLogger()

    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a StreamHandler to log to console
    handler = StreamHandler()

    # Create a formatter and set it for the handler
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    # Set the logging level for the logger
    logger.setLevel(logging.INFO)
