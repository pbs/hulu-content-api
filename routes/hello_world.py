from flask_restful import Resource

# add a hello route
class HelloWorld(Resource):
    def get(self):
        print("Hello-world accessed")
        return {
            "message": "hello flask api!"
            }