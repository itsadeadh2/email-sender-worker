class S3Client:

    def __init__(self, s3, bucket: str, logger):
        self.s3 = s3
        self.bucket = bucket
        self.logger = logger

    def download_file_to_path(self, key: str, target_path: str):
        self.logger.info(f"Downloading file {key} to {target_path}")
        try:
            self.s3.download_file(self.bucket, key, target_path)
            self.logger.info(f"File {key} downloaded successfully to {target_path}")
        except Exception as e:
            self.logger.error(f"Error downloading file {key} to {target_path}: {e}")
            raise

    def get_etag(self, key):
        try:
            self.logger.info(f"Fetching ETag for {key}")
            response = self.s3.head_object(Bucket=self.bucket, Key=key)
            current_etag = response['ETag'].strip('"')
            self.logger.info(f"ETag for {key} is {current_etag}")
            return current_etag
        except self.s3.exceptions.NoSuchKey:
            self.logger.warning(f"The object {key} does not exist in bucket {self.bucket}.")
            return None
        except Exception as e:
            self.logger.error(f"Error fetching ETag for {key}: {e}")
            raise

    def get_latest_key(self):
        self.logger.info(f"Listing objects in bucket {self.bucket}")
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket)
            if 'Contents' not in response:
                self.logger.warning(f"No objects found in bucket {self.bucket}.")
                return None

            latest_file = max(response['Contents'], key=lambda x: x['LastModified'])
            latest_file_key = latest_file['Key']

            self.logger.info(f"The latest file in the bucket '{self.bucket}' is: {latest_file_key}")
            return latest_file_key or ''
        except Exception as e:
            self.logger.error(f"Error listing objects in bucket {self.bucket}: {e}")
            raise
