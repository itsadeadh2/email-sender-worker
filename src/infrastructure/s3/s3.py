class S3Client:

    def __init__(self, s3, bucket: str):
        self.s3 = s3
        self.bucket = bucket

    def download_file_to_path(self, key: str, target_path: str):
        self.s3.download_file(self.bucket, key, target_path)

    def get_etag(self, key):
        try:
            response = self.s3.head_object(Bucket=self.bucket, Key=key)
            current_etag = response['ETag'].strip('"')
            return current_etag
        except self.s3.exceptions.NoSuchKey:
            print(f"The object {key} does not exist in bucket {self.bucket}.")
            return None

    def get_latest_key(self):
        # List objects in the bucket
        response = self.s3.list_objects_v2(Bucket=self.bucket)

        if 'Contents' not in response:
            print(f"No objects found in bucket {self.bucket}.")
            return None

        # Find the latest file based on the LastModified timestamp
        latest_file = max(response['Contents'], key=lambda x: x['LastModified'])
        latest_file_key = latest_file['Key']

        print(f"The latest file in the bucket '{self.bucket}' is: {latest_file_key}")
        return latest_file_key or ''
