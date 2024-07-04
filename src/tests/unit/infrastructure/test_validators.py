import unittest
from src.infrastructure.validators import validate_email
from src.infrastructure.exc import InvalidEmailError


class TestValidators(unittest.TestCase):

    def test_validate_email_success(self):
        mail = 'foo@baz.com'
        has_raised = False
        try:
            validate_email(mail)
        except InvalidEmailError:
            has_raised = True

        self.assertEqual(has_raised, False)

    def test_validate_email_failure(self):
        invalid_emails = ['invalid', 'invalid.com', '@invalid', 'invalid@invalid', '']

        for mail in invalid_emails:
            with self.assertRaises(InvalidEmailError):
                validate_email(mail)


if __name__ == '__main__':
    unittest.main()
