import unittest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path
from src.infrastructure.s3.s3 import S3Client
from src.infrastructure.resume.resumeprovider import ResumeProvider


class TestResumeProvider(unittest.TestCase):

    def setUp(self):
        self.mock_s3 = MagicMock(spec=S3Client)
        self.cache_folder = Path(__file__).parent / 'cache'
        self.resume_path = self.cache_folder / 'resume.pdf'
        self.etag_db = str(self.cache_folder / 'etag.db')
        self.resume_provider = ResumeProvider(s3=self.mock_s3, cache_folder=self.cache_folder, logger=MagicMock())

    @patch('shelve.open')
    def test_set_etag(self, mock_shelve_open):
        mock_db = MagicMock()
        mock_shelve_open.return_value.__enter__.return_value = mock_db

        self.resume_provider._ResumeProvider__set_etag('new-etag')

        mock_db.__setitem__.assert_called_once_with('etag', 'new-etag')

    @patch('shelve.open')
    def test_get_etag(self, mock_shelve_open):
        mock_db = MagicMock()
        mock_db.get.return_value = 'stored-etag'
        mock_shelve_open.return_value.__enter__.return_value = mock_db

        etag = self.resume_provider._ResumeProvider__get_etag()

        self.assertEqual(etag, 'stored-etag')
        mock_db.get.assert_called_once_with('etag', '')

    @patch('builtins.open', new_callable=mock_open)
    @patch.object(ResumeProvider, '_ResumeProvider__download_resume')
    def test_retrieve_with_resume_key(self, mock_download_resume, mock_open):
        self.mock_s3.get_etag.return_value = 'new-etag'
        resume_key = 'resume-key'

        result = self.resume_provider.retrieve(resume_file_key=resume_key)

        mock_download_resume.assert_called_once_with(key=resume_key)
        mock_open.assert_called_once_with(str(self.resume_path), 'rb')
        self.assertEqual(result[0], 'resume.pdf')

    @patch('builtins.open', new_callable=mock_open)
    @patch.object(ResumeProvider, '_ResumeProvider__download_resume')
    def test_retrieve_without_resume_key(self, mock_download_resume, mock_open):
        latest_key = 'latest-resume-key'
        self.mock_s3.get_latest_key.return_value = latest_key

        result = self.resume_provider.retrieve()

        mock_download_resume.assert_called_once_with(key=latest_key)
        mock_open.assert_called_once_with(str(self.resume_path), 'rb')
        self.assertEqual(result[0], 'resume.pdf')

    @patch('shelve.open')
    def test_download_resume(self, mock_shelve_open):
        mock_db = MagicMock()
        mock_shelve_open.return_value.__enter__.return_value = mock_db
        self.mock_s3.get_etag.return_value = 'new-etag'
        mock_db.get.return_value = 'old-etag'

        self.resume_provider._ResumeProvider__download_resume('resume-key')

        self.mock_s3.get_etag.assert_called_once_with(key='resume-key')
        mock_db.get.assert_called_once_with('etag', '')
        self.mock_s3.download_file_to_path.assert_called_once_with(key='resume-key', target_path=str(self.resume_path))
        mock_db.__setitem__.assert_called_once_with('etag', 'new-etag')

    @patch('shelve.open')
    def test_download_resume_cached(self, mock_shelve_open):
        mock_db = MagicMock()
        mock_shelve_open.return_value.__enter__.return_value = mock_db
        self.mock_s3.get_etag.return_value = 'same-etag'
        mock_db.get.return_value = 'same-etag'

        self.resume_provider._ResumeProvider__download_resume('resume-key')

        self.mock_s3.get_etag.assert_called_once_with(key='resume-key')
        mock_db.get.assert_called_once_with('etag', '')
        mock_shelve_open.assert_called()
        self.mock_s3.download_file_to_path.assert_not_called()
        mock_db.__setitem__.assert_not_called()


if __name__ == '__main__':
    unittest.main()
