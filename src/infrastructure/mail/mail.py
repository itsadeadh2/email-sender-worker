import requests
import os


class Mail:
    def __init__(self):
        self.domain = os.getenv("MAILGUN_DOMAIN")
        self.api_key = os.getenv("MAILGUN_API_KEY")

    def send_email(self, to, subject, text, html=None):
        response = requests.post(
            f"https://api.mailgun.net/v3/{self.domain}/messages",
            auth=("api", os.getenv("MAILGUN_API_KEY")),
            data={
                "from": f"Thiago Barbosa via MailGun <mailgun@{self.domain}>",
                "to": [to],
                "subject": subject,
                "text": text,
                "html": html
            },
        )
        if response.status_code == 200:
            return response.json()  # Assuming the response is in JSON format
        else:
            response.raise_for_status()
