from flask import Flask
from flask_restful import Resource,Api

app = Flask(__name__)
api = Api(app)


class GoldEndpoint(Resource):

    def get(self, quarter, subject):
        return {quarter:subject}


api.add_resource(GoldEndpoint,'/goldapi/<quarter>/<subject>')

if __name__ == '__main__':
    app.run()



