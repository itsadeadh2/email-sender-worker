import unittest
from unittest.mock import patch, Mock
from src.infrastructure.mail.mail import Mail


class TestMail(unittest.TestCase):

    @patch('src.infrastructure.mail.mail.requests')
    def test_send_email_success(self, requests_mock):
        dummy_domain = 'foo.baz.com'
        dummy_api_key = 'myapikey'
        dummy_to = 'foo@baz.com'
        dummy_subject = 'My Test Email'
        dummy_text = 'Hi this is a test email'
        dummy_html = 'Null'

        expected_call_uri = f"https://api.mailgun.net/v3/{dummy_domain}/messages"
        expected_call_kwargs = {
            'auth': ("api", dummy_api_key),
            'data': {
                "from": f"Thiago Barbosa via MailGun <mailgun@{dummy_domain}>",
                "to": [dummy_to],
                "subject": dummy_subject,
                "text": dummy_text,
                "html": dummy_html
            }
        }

        dummy_response = Mock()
        dummy_response.status_code = 200

        requests_mock.post.return_value = dummy_response

        mail = Mail(domain=dummy_domain, api_key=dummy_api_key)
        mail.send_email(to=dummy_to, subject=dummy_subject, text=dummy_text, html=dummy_html)

        requests_mock.post.assert_called_with(expected_call_uri, **expected_call_kwargs)
        dummy_response.json.assert_called_once()

    @patch('src.infrastructure.mail.mail.requests')
    def test_send_email_failure(self, requestsMock):
        dummy_domain = 'foo.baz.com'
        dummy_api_key = 'myapikey'
        dummy_to = 'foo@baz.com'
        dummy_subject = 'My Test Email'
        dummy_text = 'Hi this is a test email'
        dummy_html = 'Null'

        expected_call_uri = f"https://api.mailgun.net/v3/{dummy_domain}/messages"
        expected_call_kwargs = {
            'auth': ("api", dummy_api_key),
            'data': {
                "from": f"Thiago Barbosa via MailGun <mailgun@{dummy_domain}>",
                "to": [dummy_to],
                "subject": dummy_subject,
                "text": dummy_text,
                "html": dummy_html
            }
        }

        dummy_response = Mock()
        dummy_response.status_code = 500

        requestsMock.post.return_value = dummy_response

        mail = Mail(domain=dummy_domain, api_key=dummy_api_key)
        mail.send_email(to=dummy_to, subject=dummy_subject, text=dummy_text, html=dummy_html)

        requestsMock.post.assert_called_with(expected_call_uri, **expected_call_kwargs)
        dummy_response.raise_for_status.assert_called_once()


if __name__ == '__main__':
    unittest.main()
