from flask import Flask
from flask_restful import Resource,Api

app = Flask(__name__)
api = Api(app)
# TODO: Consider using more user-friendly codes for quarters and subjects on user side, keep hash table on server side ?


class GoldEndpoint(Resource):
    # TODO: Once get_course_listing is implemented, modify get request to return json response to client
    # TODO: Implement error catching when user sends in invalid quarter, course subject, or login credentials

    def get(self, quarter, subject):
        return {quarter:subject}


api.add_resource(GoldEndpoint,'/goldapi/<quarter>/<subject>')

if __name__ == '__main__':
    app.run()



