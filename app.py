from datetime import datetime
from flask_caching import Cache
from flask import Flask, redirect
from flask_restful import Api, Resource
from flask import request
from model import db, Url
import string
import random
from urlvalidator import URLValidator, ValidationError

app = Flask(__name__)
cache = Cache()
api = Api(app)
validate = URLValidator()
cache.init_app(app, config={'CACHE_TYPE': 'simple'})


# for meaning of cache is very good
# http://www.mit.edu/~yandros/doc/cache_doc.html#:~:text=By%20default%2C%20pages%20protected%20with,allow%20them%20to%20be%20cached.
# for using cache is useful
# https://flask-caching.readthedocs.io/en/latest/
def random_generator(size=5, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for x in range(size))


class Get_url(Resource):
    def post(self):
        try:
            # get url param from request
            long_url = request.args.get('url')
            # get time param from url time can be null
            time = request.args.get('time')
            # check that url has a true value
            validate(long_url)
            # make a random short string
            short_url = random_generator()
            # make a new object from url model
            url = Url()
            # if time doesn't null convert string to a datetime object
            if time is not None:
                url.pub_date = datetime.strptime(time, '%Y-%m-%d %H:%M')
            url.long_url = long_url
            url.short_url = short_url
            db.session.add(url)
            db.session.commit()
            # if process doesn't have any error we return the short url in format of jason to user
            return {'short_url': short_url}
        except ValidationError:
            return {'error': 'an error has occurred'}
        except Exception:
            return {'error': 'wrong format time error'}


class Redirect(Resource):
    def get(self, url):
        # get object with unique field
        # it really has value in it the value is a query perhaps it has some object in condition of that query
        exist_url = Url.query.filter_by(short_url=url)
        # check that we have object
        if exist_url.count() == 1:
            # check the expire of time
            if exist_url[0].pub_date is None or exist_url[0].pub_date > datetime.now():
                count = exist_url[0].counter
                exist_url[0].counter = count + 1
                db.session.commit()
                # if everything is ok redirect user to long url
                return redirect(exist_url[0].long_url, 302)
        return {'error': 'an error has occurred'}


class Aggregation(Resource):
    @cache.cached(timeout=180, key_prefix='all_data')
    def get(self):
        data_list = []
        data = Url.query.order_by(Url.counter).all()
        for item in data:
            data_list.append({'Your_url': item.long_url, 'Our_url': item.short_url, 'counter': item.counter})
        return {'document': data_list}

    cached_data = get('/aggregation')

    def post(self):
        url = request.args.get('url')
        exist_url = Url.query.filter_by(short_url=url)
        if exist_url.count() == 1:
            return {'the counter of your url': exist_url[0].counter}

        return {'error': exist_url.count()}


api.add_resource(Redirect, '/<string:url>')
# Your view names need to be unique even if they are pointing to the same view method
api.add_resource(Get_url, '/')
api.add_resource(Aggregation, '/aggregation')
if __name__ == '__main__':
    app.run(debug=True)
