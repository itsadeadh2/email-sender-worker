import io
import unittest
from unittest.mock import MagicMock, patch

from src.infrastructure.resume.resumeprovider import ResumeProvider


class TestResumeProvider(unittest.TestCase):

    def setUp(self):
        self.resume_provider = ResumeProvider(logger=MagicMock())

    @patch('src.infrastructure.resume.resumeprovider.requests')
    @patch('src.infrastructure.resume.resumeprovider.HTML')
    def test_download_and_parse_resume(self, html_mock, requests_mock):
        key, content = self.resume_provider.retrieve()
        resume_text = requests_mock.get.return_value.text
        requests_mock.get.assert_called_once_with('https://resume.itsadeadh2.com')
        html_mock.assert_called_once_with(string=resume_text)
        self.assertEqual(key, 'resume.pdf')
        self.assertTrue(isinstance(content, io.TextIOWrapper))


if __name__ == '__main__':
    unittest.main()
