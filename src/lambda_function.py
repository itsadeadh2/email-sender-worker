import os

from dotenv import load_dotenv

from src.domain import ContactInfoHandler
from src.infrastructure.logger import create_logger
from src.infrastructure.mail.mail import Mail
from src.infrastructure.resume.resumeprovider import ResumeProvider

logger = create_logger()


def get_handler():
    mg_domain = os.getenv("MAILGUN_DOMAIN")
    mg_api_key = os.getenv("MAILGUN_API_KEY")

    mail = Mail(domain=mg_domain, api_key=mg_api_key, logger=logger)

    resume = ResumeProvider(logger=logger)

    return ContactInfoHandler(mail=mail, resume=resume, logger=logger)


def handle(event, context):
    _handler = get_handler()

    logger.info("Received event: " + str(event))
    for message in event['Records']:
        _handler.handle(message=message)


if __name__ == "__main__":
    load_dotenv()
    handler = get_handler()
    handler.handle(message={"body": "itsadeadh2@gmail.com"})