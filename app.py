from flask import Flask, redirect
from flask_restful import Api, Resource
from flask import request

import string
import random

from urlvalidator import ValidationError, URLValidator

app = Flask(__name__)

api = Api(app)
validate = URLValidator()


def random_generator(size=5, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for x in range(size))


dict_url = {}


class Get_url(Resource):
    def post(self):
        try:
            validate(request.args.get('url'))
            short_url = random_generator()
            dict_url[short_url] = request.args.get('url')
            return {'short_url': short_url}
        except ValidationError as exception:
            return {'error': 'it is not url'}


class Redirect(Resource):
    def get(self, url):
        if url in dict_url:
            return redirect(dict_url[url], 302)
        return {'error': 'an error has occurred'}


api.add_resource(Redirect, '/<string:url>')
api.add_resource(Get_url, '/')

if __name__ == '__main__':
    app.run()
