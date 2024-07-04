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

    def __init__(self, s3: S3Client, cache_folder: Path, logger):
        self.__s3 = s3
        self.__cache_folder = cache_folder
        self.__resume_path = self.__cache_folder / 'resume.pdf'
        self.__etag_db = str(self.__cache_folder / 'etag.db')
        self.__logger = logger

    def __set_etag(self, etag):
        self.__logger.debug(f"Setting ETag in cache: {etag}")
        with shelve.open(self.__etag_db) as db:
            db['etag'] = etag or ''

    def __get_etag(self):
        self.__logger.debug("Getting ETag from cache")
        with shelve.open(self.__etag_db) as db:
            etag = db.get('etag', '')
        self.__logger.debug(f"Retrieved ETag from cache: {etag}")
        return etag

    def __download_resume(self, key: str):
        self.__logger.info(f"Checking if resume with key {key} needs to be downloaded")
        target_resume_etag = self.__s3.get_etag(key=key)
        is_resume_cached = target_resume_etag == self.__get_etag()

        if is_resume_cached:
            self.__logger.info(f"Resume with key {key} is already cached")
            return

        self.__logger.info(f"Downloading resume with key {key}")
        self.__s3.download_file_to_path(key=key, target_path=str(self.__resume_path))
        self.__set_etag(target_resume_etag)
        self.__logger.info(f"Resume with key {key} downloaded and cached")

    def retrieve(self, resume_file_key: str = None) -> tuple:
        self.__logger.info(f"Retrieving resume with file key: {resume_file_key}")
        resume_key = resume_file_key
        if not resume_key:
            self.__logger.info("No file key provided, fetching the latest key")
            resume_key = self.__s3.get_latest_key()

        self.__download_resume(key=resume_key)

        self.__logger.info(f"Returning resume file: resume.pdf")
        return 'resume.pdf', open(str(self.__resume_path), 'rb')
