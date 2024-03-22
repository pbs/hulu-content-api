from flask_restful import Resource

# simple endpoint to quickly test if API is running
class HelloWorld(Resource):
    def get(self):
        print("Hello-world accessed")
        return {
            "message": "hello flask api!"
            }