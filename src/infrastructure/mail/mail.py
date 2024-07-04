import requests


class Mail:
    def __init__(self, domain, api_key):
        self.domain = domain
        self.api_key = api_key

    def send_email(self, to, subject, text, html=None, files: dict = None):
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
            return response.json()  # Assuming the response is in JSON format
        else:
            response.raise_for_status()
