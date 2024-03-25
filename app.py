import os 
from flask import Flask, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from config.logger import configure_logger
from routes.hello_world import HelloWorld
from routes.authenticate import Authenticate
from routes.content_portal import ContentPortal


## ------ BASIC CONFIG ------ ##
load_dotenv()

# define app and api 
app = Flask(__name__)

# configure JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
JWT = JWTManager(app)

# set api 
api = Api(app)

## ------ LOGGING ------ ##

logger = configure_logger()

@app.before_request
def log_request_info():
    logger.info(
        f"Request received - Method: {request.method}, Path: {request.path}, User: {request.remote_addr}"
    )

@app.after_request
def log_response_info(response):
    response_data = response.get_json()
    logger.info(
        f"Response sent - Status: {response.status_code}"
    )
    if response_data is not None:
        if "message" in response_data:
            logger.info(
                f"Response message: {response_data['message']}"
            )
        if "user" in response_data:
            logger.info(
                f"User: {response_data['user']}"
            )
    return response

## ------ ENDPOINTS ------ ##

api.add_resource(HelloWorld, "/")
api.add_resource(Authenticate, "/authenticate")
api.add_resource(ContentPortal, "/content_portal")


## ------ RUN APPLICATION ------ ##
if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=8080,
            debug=True)