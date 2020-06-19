from flask import Flask, redirect
from flask_restful import Api, Resource
from flask import request
from model import db, Url

import string
import random

from urlvalidator import ValidationError, URLValidator

app = Flask(__name__)

api = Api(app)
validate = URLValidator()

app.config['SECRET_KEY'] = 'mysecretkey'

def random_generator(size=5, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for x in range(size))


dict_url = {}


class Get_url(Resource):
    def post(self):
        try:
            long_url = request.args.get('url')
            validate(long_url)
            short_url = random_generator()
            url = Url(long_url, short_url)
            db.session.add(url)
            db.session.commit()
            return {'short_url': short_url}
        except ValidationError as exception:
            return {'error': 'it is not url'}


class Redirect(Resource):
    def get(self, url):
        exist_url = Url.query.filter_by(short_url=url)
        if exist_url is not None and exist_url.count() == 1:
            return redirect(exist_url[0].long_url, 302)
        return {'error': 'an error has occurred'}


api.add_resource(Redirect, '/<string:url>')
api.add_resource(Get_url, '/')

if __name__ == '__main__':
    app.run(debug=True)
