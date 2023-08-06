import os
import boto3 as boto

class S3Client(object):
    def __init__(self, bucket_name):
        self.client = boto.resource('s3', endpoint_url='http://localhost:4566',
            aws_access_key_id = 'test',
            aws_secret_access_key = 'test')
        self.bucket_name = bucket_name

    def __create_bucket(self):
        """Create bucket in remote s3
        """
        self.client.create_bucket(Bucket=self.bucket_name)


    def __print_all_buckets(self):
        """Prints all bucket available in remote s3
        """
        for bucket in self.client.buckets.all():
            print(bucket.name)

    def view(self):
        """Prints all objects presents in current bucket
        """
        bucket_instance = self.client.Bucket(self.bucket_name)
        for obj in bucket_instance.objects.all():
            print(obj.key)

    def download(self, s3_path: str, dst_path: str):
        """Downloads file to local cache

        Args:
            s3_path (str): path to file in remote bucket
            dst_path (str): path of file in local location
        """
        bucket_instance = self.client.Bucket(self.bucket_name)
        bucket_instance.download_file(Key=s3_path, Filename=dst_path)
        print(f"File {s3_path} transferred to {dst_path}.")

    def upload(self, content: str, target: str):
        """Uploads a given UTF-8 content to remote target

        Args:
            content (str): string content to wite in remote bucket
            target (str): location in remote file to write content to
        """
        self.client.Object(self.bucket_name, target).put(Body=content)