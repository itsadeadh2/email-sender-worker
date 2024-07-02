import os
from src.domain import ContactInfoHandler
from src.infrastructure.mail.mail import Mail


def handler(event, context):
    mg_domain = os.getenv("MAILGUN_DOMAIN")
    mg_api_key = os.getenv("MAILGUN_API_KEY")

    mail = Mail(domain=mg_domain, api_key=mg_api_key)
    _handler = ContactInfoHandler(mail=mail)

    print("Received event: " + str(event))
    for message in event['Records']:
        _handler.handle(message=message)
