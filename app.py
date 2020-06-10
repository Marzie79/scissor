from flask import Flask
from flask_restful import Api, Resource
from flask import request

import string
import random

app = Flask(__name__)

api = Api(app)


def random_generator(size=5, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for x in range(size))


class First(Resource):
    def post(self):
        # I give a param with key url for sending data
        url = request.args.get('url')
        if url[0:7] == 'http://' or url[0:8] == 'https://':
            return {'short_url': random_generator()}
        return {'error': 'it is not url'}


api.add_resource(First, '/')

if __name__ == '__main__':
    app.run()
