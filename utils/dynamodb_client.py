import boto3

class DynamoDBClient:
    def __init__(self, aws_access_key_id, aws_secret_acceess_key):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_acceess_key = aws_secret_acceess_key
        self.client = boto3.resource("dynamodb", 
                                     aws_access_key_id=self.aws_access_key_id,
                                     aws_secret_acceess_key=self.aws_secret_acceess_key,
                                     region_name="us-east-1"
                                     )
    
    def validate_user(self, username, password):
        # connect to table
        users = self.client.Table("hulu-content-portal-api-users")
        # retrieve user infomraiton
        response = users.get_item(Key={"username": username})
        # validate credentials 
        if "Item" in response:
            data = response["Item"]
            if data["password"] == password:
                return True, data
        return False, None
    
    def update_user_token(self, username, api_token):
        # connect to table 
        users = self.client.Table("hulu-content-portal-api-users")
        # update the entry 
        users.update_item(
            Key={"username": username},
            UpdateExpression="SET api_token = :val",
            ExpressionAttributeValues={":val": api_token}
        )

        