from flask import Flask
from flask_restful import Resource,Api
from scraper import Scraper

app = Flask(__name__)
api = Api(app)
# TODO: Implement dictionary to convert custom quarter/subject codes to actual ones


class GoldEndpoint(Resource):
    # TODO: Implement error catching when user sends in invalid quarter, course subject, or login credentials
    def get(self, quarter, subject):
        gold = Scraper(quarter,subject)
        response = gold.get_course_listings()
        return response


api.add_resource(GoldEndpoint,'/goldapi/<quarter>/<subject>')

if __name__ == '__main__':
    app.run()



