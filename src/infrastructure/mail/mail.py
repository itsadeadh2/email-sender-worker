import requests


class Mail:
    def __init__(self, domain, api_key, logger):
        self.domain = domain
        self.api_key = api_key
        self.logger = logger

    def send_email(self, to, subject, text, html=None, files: dict = None):
        self.logger.info(f"Preparing to send email to {to} with subject: {subject}")

        try:
            response = requests.post(
                f"https://api.mailgun.net/v3/{self.domain}/messages",
                auth=("api", self.api_key),
                files=files,
                data={
                    "from": f"Thiago Barbosa via MailGun <mailgun@{self.domain}>",
                    "to": [to],
                    "subject": subject,
                    "text": text,
                    "html": html
                },
            )
            if response.status_code == 200:
                self.logger.info(f"Email sent successfully to {to}")
                return response.json()  # Assuming the response is in JSON format
            else:
                self.logger.warning(f"Failed to send email to {to}, status code: {response.status_code}")
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while sending email to {to}: {e}")
            raise
