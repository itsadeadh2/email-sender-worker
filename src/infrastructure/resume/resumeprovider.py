from pathlib import Path
import shelve
from src.infrastructure.s3.s3 import S3Client


class ResumeProvider:
    """
    This class also has a cache solution, but since it runs on a lambda
    that isn't really going to be used.
    I'll keep it in here for now in case I ever decide to move this to
    a runner that has a dedicated file system or add EFS to lambda.
    """

    def __init__(self, s3: S3Client, cache_folder: Path):
        self.__s3 = s3
        self.__cache_folder = cache_folder
        self.__resume_path = self.__cache_folder / 'resume.pdf'
        self.__etag_db = str(self.__cache_folder / 'etag.db')

    def __set_etag(self, etag):
        with shelve.open(self.__etag_db) as db:
            db['etag'] = etag or ''

    def __get_etag(self):
        with shelve.open(self.__etag_db) as db:
            return db.get('etag', '')

    def __download_resume(self, key: str):
        target_resume_etag = self.__s3.get_etag(key=key)
        is_resume_cached = target_resume_etag == self.__get_etag()

        if is_resume_cached:
            return
        self.__s3.download_file_to_path(key=key, target_path=str(self.__resume_path))
        self.__set_etag(target_resume_etag)

    def retrieve(self, resume_file_key: str = None) -> tuple:
        resume_key = resume_file_key
        if not resume_key:
            resume_key = self.__s3.get_latest_key()

        self.__download_resume(key=resume_key)

        return 'resume.pdf', open(str(self.__resume_path), 'rb')
