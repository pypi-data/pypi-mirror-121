import os
import re
import pandas as pd
from onpremgpusdk.data.__s3util__ import S3Client
from botocore import exceptions
from pathlib import Path


LOCAL_BUCKET_PATH = os.path.join(str(Path.home()), ".onpremgpusdk")

class DataInstance(S3Client):

    def __init__(self, bucket_name: str):
        super(DataInstance, self).__init__(bucket_name)

    def write_csv(self, df: pd.DataFrame, target: str):
        """Writes a dataframe to remote bucket and update data in local file for consistency

        Args:
            df (pd.DataFrame): Dataframe to write to remote bucket
            target (str): target to write file to in remote bucket
        """
        csv_content = df.to_csv()
        self.upload(csv_content, target)

        # Update local cache
        localFilePath = self.__create_path(target)
        with open(localFilePath, 'w+') as localCacheFile:
            localCacheFile.write(csv_content)

    def read_csv(self, path: str) -> pd.DataFrame:
        """Reads csv file to Data fram from cache or remote bucket

        Args:
            path (str): Path of file in remote bucket

        Returns:
            pd.DataFrame: Data frame of the csv to read 
        """
        filePath = self.__create_path(path)
        if(os.path.isfile(filePath)):
            print("Reading data from cache")
            return pd.read_csv(filePath)
        else:
            print(f"Fetching data from {self.bucket_name}")
            return self.__refresh_from_bucket(path, filePath)

    def __create_path(self, path: str) -> str:
        """ Creates local path from remote path 

        Args:
            path (str): Path of file in remote bucket

        Returns:
            str: Path of the file in local cache
        """

        filePath = os.path.join(LOCAL_BUCKET_PATH, self.bucket_name, path)
        if not os.path.exists(os.path.dirname(filePath)):
            # Create folders if doesn't exist
            os.makedirs(os.path.dirname(filePath), exist_ok=True)
        return filePath

    def __refresh_from_bucket(self, path: str, filePath: str) -> pd.DataFrame:
        """ Refreshes and returns content from remote bucket

        Args:
            path (str): Path of file in remote bucket
            filePath (str): Path of file in local machine

        Raises:
            e: is raised in case of unknown 

        Returns:
            pd.DataFrame: Data frame of the csv to read 
        """

        try:
            self.download(path, filePath)
            return pd.read_csv(filePath)
        except exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print(f"File not found in remote bucket {self.bucket_name}")
            else:
                raise e