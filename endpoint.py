from flask import Flask
from flask_restful import Resource,Api
import goldScraper


app = Flask(__name__)
api = Api(app)


class GoldEndpoint(Resource):
    # TODO: Implement error catching when user sends in invalid quarter, course subject, or login credentials
    def get(self, quarter, subject):
        response = goldScraper.get_courses(quarter, subject)
        return response


api.add_resource(GoldEndpoint,'/goldapi/<quarter>/<subject>')

if __name__ == '__main__':
    app.run()



