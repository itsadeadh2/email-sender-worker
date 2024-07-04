import unittest
from unittest.mock import patch, Mock
from src.domain.handlers import ContactInfoHandler


class TestContactHandler(unittest.TestCase):

    @patch('src.domain.handlers.ContactInfoParser')
    @patch('src.domain.handlers.validate_email')
    def test_handle(self, validator_mock, contact_parser_mock):
        parser_instance = Mock()
        contact_parser_mock.return_value = parser_instance
        mail_mock = Mock()
        resume_mock = Mock()

        dummy_parsed_text = 'foo'
        dummy_parsed_html = '<h1>foo</h1>'
        dummy_email = 'foo@baz.com'
        dummy_message = {
            'body': dummy_email
        }
        mock_resume_file = resume_mock.retrieve.return_value
        dummy_attachments = {
            'attachment': mock_resume_file
        }

        parser_instance.get_html.return_value = dummy_parsed_html
        parser_instance.get_text.return_value = dummy_parsed_text

        handler = ContactInfoHandler(mail=mail_mock, resume=resume_mock)
        handler.handle(message=dummy_message)

        mail_mock.send_email.assert_called_with(
            to=dummy_email,
            subject="Contact Information - Thiago Barbosa",
            text=dummy_parsed_text,
            html=dummy_parsed_html,
            files=dummy_attachments
        )
        validator_mock.assert_called_with(dummy_email)


if __name__ == '__main__':
    unittest.main()
