import os
import boto3
from pathlib import Path
from src.domain import ContactInfoHandler
from src.infrastructure.mail.mail import Mail
from src.infrastructure.resume.resumeprovider import ResumeProvider
from src.infrastructure.s3.s3 import S3Client
from src.infrastructure.logger import create_logger

logger = create_logger()


def get_handler():
    mg_domain = os.getenv("MAILGUN_DOMAIN")
    mg_api_key = os.getenv("MAILGUN_API_KEY")
    resumes_bucket = os.getenv("RESUMES_BUCKET")

    mail = Mail(domain=mg_domain, api_key=mg_api_key, logger=logger)

    s3 = boto3.client('s3')
    s3_client = S3Client(s3=s3, bucket=resumes_bucket, logger=logger)

    cache_path = Path('/tmp')

    resume = ResumeProvider(s3=s3_client, cache_folder=cache_path, logger=logger)

    return ContactInfoHandler(mail=mail, resume=resume, logger=logger)


def handler(event, context):
    _handler = get_handler()

    logger.info("Received event: " + str(event))
    for message in event['Records']:
        _handler.handle(message=message)
