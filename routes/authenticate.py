from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
import os 

from utils.dynamodb_client import DynamoDBClient

class Authenticate(Resource):
    def post(self):
        # get information from request 
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # check if request contained any credentials 
        if not (username and password):
            return {
                "message": "Username and password are required."
            }, 400
        
        # instantiate dynamodb client 
        dynamodb = DynamoDBClient(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_acceess_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        # validate credentails 
        is_valid_user, user_data = dynamodb.validate_user(
            username=username,
            password=password
        )

        # if user is validated - provide a token and update db 
        if is_valid_user:
            api_token = create_access_token(identity=username)
            dynamodb.update_user_token(
                username=username, 
                api_token=api_token
            )
            return {
                "payload": api_token, 
                "message": "Token generation successful", 
                "user": username
            }, 200
        else:
            return {
                "payload": None, 
                "message": "Invalid username or password",
                "user": username
            }, 401


            
