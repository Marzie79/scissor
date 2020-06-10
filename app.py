from flask import Flask
from flask_restful import Api, Resource
from urllib.parse import quote_plus

import string
import random

app = Flask(__name__)

api = Api(app)


def random_generator(size=6, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for x in range(size))


class First(Resource):
    def post(self, url):
        print(url[0:7])
        if url[0:7] == 'http://' or url[0:8] == 'https://':
            return {'short_url': random_generator()}
        return {'error': 'it is not url'}


api.add_resource(First, '/<string:url>')

if __name__ == '__main__':
    app.run()
