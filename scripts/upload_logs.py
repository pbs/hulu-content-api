import os 
from datetime import datetime 
from utils.s3_client import S3Client
from dotenv import load_dotenv

load_dotenv()

# check if its a new day 
def is_new_day(last_upload_date):
    today = datetime.now().date()
    return today > last_upload_date

def main():
    # initialize s3 client 
    s3 = S3Client(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    # load the last update

    # set path to log file 
    filepath = os.path.join("logs", "api.log")

    # upload to s3
    try:
        s3.upload_logs(filepath)
        print("Logs successfully uploaded")
    except Exception as e:
        print(f"Error uploading logs to S3: {str(e)}")

# run 
if __name__ == "__main__":
    main()
