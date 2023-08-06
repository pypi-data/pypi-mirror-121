import os
import pandas as pd
from onpremgpusdk.data.__s3util__ import S3Client
from botocore import exceptions


LOCAL_BUCKET_PATH = "/tmp/"

class DataInstance(S3Client):

    def __init__(self, bucket_name: str):
        super(DataInstance, self).__init__(bucket_name)

    def write_csv(self, df: pd.DataFrame, target: str):
        csv_content = df.to_csv()
        self.upload(csv_content, target)

    def read_csv(self, path):
        filePath = LOCAL_BUCKET_PATH + path
        if(os.path.isfile(filePath)):
            print("Reading data from cache")
            pd.read_csv(filePath)
        else:
            try:
                self.download(path,filePath)
                pd.read_csv(filePath)
            except exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print(f"File not found in remote bucket {self.bucket_name}")
                else:
                    raise
