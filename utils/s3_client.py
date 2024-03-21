import boto3
from datetime import datetime

class S3Client:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.client = boto3.resource("s3", 
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key,
                                     region_name="us-east-1")
        
    def upload_logs(self, log_file):
        formatted_date = datetime.today().strftime("%m%d%y")
        s3_key = f"logs_{formatted_date}.log"

        try:
            self.client.upload_file(
                filename=log_file, 
                Bucket="hulu-content-portal-api-logs", 
                Key = s3_key
            )
        except Exception as e:
            print(f"Error uploading object: {str(e)}")
        