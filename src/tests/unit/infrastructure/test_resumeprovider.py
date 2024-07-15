import unittest
from unittest.mock import MagicMock, patch

from src.infrastructure.resume.resumeprovider import ResumeProvider


class TestResumeProvider(unittest.TestCase):

    def setUp(self):
        self.resume_provider = ResumeProvider(logger=MagicMock())

    @patch('builtins.open')
    @patch('src.infrastructure.resume.resumeprovider.pdfkit')
    def test_download_and_parse_resume(self, pdfkit_mock, open_mock):
        key, content = self.resume_provider.retrieve()
        pdfkit_mock.configuration.assert_called_once_with(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        pdfkit_mock.from_url.assert_called_once_with('https://resume.itsadeadh2.com', 'resume.pdf',
                                                     configuration=pdfkit_mock.configuration.return_value)
        open_mock.assert_called_once_with('resume.pdf', 'rb')
        self.assertEqual(key, 'resume.pdf')


if __name__ == '__main__':
    unittest.main()
