from abc import ABC

from src.infrastructure.mail.mail import Mail
from src.infrastructure.mail.templates.parsers import ContactInfoParser
from src.infrastructure.validators import validate_email
from src.infrastructure.resume.resumeprovider import ResumeProvider


class Handler(ABC):
    def handle(self, message):
        pass


class ContactInfoHandler(Handler):
    def __init__(
            self,
            mail: Mail,
            resume: ResumeProvider
    ):
        self.mail = mail
        self.resume = resume

    def handle(self, message):
        email = message.get('body')
        print(f'Received email: {str(email)}')
        validate_email(email)

        resume_file_data = self.resume.retrieve()
        attachments = {
            'attachment': resume_file_data
        }

        # retrieve additional information
        parser = ContactInfoParser()
        html = parser.get_html()
        text = parser.get_text()
        self.mail.send_email(
            to=email,
            subject="Contact Information - Thiago Barbosa",
            text=text,
            html=html,
            files=attachments
        )
