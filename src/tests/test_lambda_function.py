import os
import unittest
from unittest.mock import patch
from src.lambda_function import handler


class TestHandler(unittest.TestCase):

    @patch('src.lambda_function.ContactInfoHandler')
    @patch('src.lambda_function.Mail')
    @patch('src.lambda_function.ResumeProvider')
    @patch('src.lambda_function.logger')
    def test_handler(self, mock_logger_instance, MockResume, MockMail, MockContactInfoHandler):
        # Set up environment variables
        os.environ['MAILGUN_DOMAIN'] = 'test_domain'
        os.environ['MAILGUN_API_KEY'] = 'test_api_key'

        # Create a mock Mail instance
        mock_mail_instance = MockMail.return_value
        mock_resume_instance = MockResume.return_value

        # Create a mock ContactInfoHandler instance
        mock_contact_info_handler_instance = MockContactInfoHandler.return_value

        # Create a mock event
        mock_event = {
            'Records': [
                {'message': 'test_message_1'},
                {'message': 'test_message_2'}
            ]
        }
        mock_context = {}  # Context is not used in this handler

        # Call the handler function
        handler(mock_event, mock_context)

        # Assertions
        MockMail.assert_called_once_with(domain='test_domain', api_key='test_api_key', logger=mock_logger_instance)
        MockContactInfoHandler.assert_called_once_with(mail=mock_mail_instance, resume=mock_resume_instance, logger=mock_logger_instance)

        # Assert that the handle method was called for each message
        calls = [unittest.mock.call(message={'message': 'test_message_1'}),
                 unittest.mock.call(message={'message': 'test_message_2'})]
        mock_contact_info_handler_instance.handle.assert_has_calls(calls, any_order=True)


if __name__ == '__main__':
    unittest.main()
