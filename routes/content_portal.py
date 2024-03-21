from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from jwt.exceptions import InvalidTokenError
import os 
from dotenv import load_dotenv

from config.parser import configure_parser
from utils.hulu_content_portal_client import HuluContentClient

load_dotenv()

class ContentPortal(Resource):
    def post(self):
        try:
            # JWT verification and identity resolution
            verify_jwt_in_request()
            current_user = get_jwt_identity()

            # initialize parser and grab arguments
            parser = configure_parser()
            args = parser.parse_args()


            # call content client 
            try:
                # instantiate client 
                hulu = HuluContentClient(
                    executable_path="/opt/homebrew/bin/chromedriver"
                )
                # login 
                hulu.login(
                    email=os.getenv("HULU_CONTENT_USERNAME"),
                    password=os.getenv("HULU_CONTENT_PASSWORD")
                )
                # generate report 
                hulu.get_metrics(**args)

                return {
                    "payload": None, 
                    "message": "Successfully submitted report request!", 
                    "user": current_user
                }, 200
            
            except Exception as e:
                return {
                    "paylod": None, 
                    "message": f"Error in ContentPortal post method: {str(e)}", 
                    "user": current_user
                }, 500
        
        except InvalidTokenError as e:
            return {
                "payload": None, 
                "message": f"Invalid API token: {str(e)}",
                "user": current_user
            }
        except Exception as e:
            return {
                "payload": None, 
                "message": f"Error submitting report request: {str(e)}", 
                "user": current_user
            }, 500

