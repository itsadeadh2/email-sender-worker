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
            resume: ResumeProvider,
            logger
    ):
        self.mail = mail
        self.resume = resume
        self.logger = logger

    def handle(self, message):
        email = message.get('body')
        self.logger.info(f"Received email: {str(email)}")
        try:
            validate_email(email)
            self.logger.info(f"Email {email} validated successfully")
        except ValueError as e:
            self.logger.error(f"Validation error for email {email}: {e}")
            raise

        try:
            resume_file_data = self.resume.retrieve()
            self.logger.info("Resume retrieved successfully")
        except Exception as e:
            self.logger.error(f"Error retrieving resume: {e}")
            raise

        attachments = {
            'attachment': resume_file_data
        }

        try:
            parser = ContactInfoParser()
            html = parser.get_html()
            text = parser.get_text()
            self.logger.info("Parsed contact information successfully")
        except Exception as e:
            self.logger.error(f"Error parsing contact information: {e}")
            raise

        try:
            self.mail.send_email(
                to=email,
                subject="Contact Information - Thiago Barbosa",
                text=text,
                html=html,
                files=attachments
            )
            self.logger.info(f"Email sent successfully to {email}")
        except Exception as e:
            self.logger.error(f"Error sending email to {email}: {e}")
            raise
