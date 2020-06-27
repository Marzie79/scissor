import json
import unittest
from app import app
from model import Url

app.testing = True


class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_true_url_without_time(self):
        response = app.test_client().post(
            '/?url=http://adshjkl.ir'
        )
        data = response.get_data('url')
        res = json.loads(data)
        self.assertIn('short_url', res)

    def test_none_url(self):
        response = app.test_client().post(
            '/?url=http://'
        )
        data = response.get_data('url')
        res = json.loads(data)
        self.assertIn('error', res)

    def test_short_url(self):
        response = app.test_client().post(
            '/?url=http://k.com'
        )
        data = response.get_data('url')
        res = json.loads(data)
        self.assertIn('short_url', res)

    def test_noHost_url(self):
        response = app.test_client().post(
            '/?url=http://.com'
        )
        data = response.get_data('url')
        res = json.loads(data)
        self.assertIn('error', res)

    def test_correct_redirecting(self):
        response = app.test_client().post(
            '/?url=http://google.com'
        )
        data = response.get_data('url')
        res = json.loads(data)
        response1 = app.test_client().get(res['short_url'])
        self.assertEqual(response1.status_code, 302)

    def test_wrong_url_redirecting(self):
        response1 = app.test_client().get('hello')
        self.assertEqual(response1.status_code, 200)

    def test_end_of_date_from_database(self):
        response = app.test_client().get('Ztkoq')
        self.assertEqual(response.status_code, 200)

    def test_make_full_correct_request(self):
        response = app.test_client().post('/?url=https://google.com&time=2090-06-19 03:39')
        data = response.get_data('url')
        print(data)
        res = json.loads(data)
        response1 = app.test_client().get(res['short_url'])
        self.assertEqual(response1.status_code, 302)

    def test_make_request_with_wrong_time(self):
        response = app.test_client().post('/?url=https://google.com&time=2090-019 03:39')
        data = response.get_data('url')
        res = json.loads(data)
        self.assertIn('error', res)

    # at first the value of all url should be 0
    def test_counter_in_first(self):
        response = app.test_client().post('/?url=https://hello.com&time=2090-06-19 03:39')
        data = response.get_data('url')
        res = json.loads(data)
        exist_url = Url.query.filter_by(short_url=res['short_url'])
        self.assertEqual('0', str(exist_url[0].counter))

    # at first we get the counter of an existing object and we use it short url and check the counter again the counter should be changed
    def test_counter_in_for_using_a_lot(self):
        exist_url = Url.query.filter_by(short_url='TYUDX')
        first = str(exist_url[0].counter + 1)
        response = app.test_client().get('TYUDX')
        second = str(exist_url[0].counter)
        self.assertEqual(first, second)

    def test_aggregation_get_method(self):
        response = app.test_client().get('/aggregation')
        data = response.get_data('document')
        res = json.loads(data)
        self.assertIn('document', res)

    def test_aggregation_correct_post(self):
        response = app.test_client().post('/aggregation?url=VzJeW')
        data = response.get_data('the counter of your url')
        res = json.loads(data)
        self.assertIn('the counter of your url', res)

    def test_aggregation_wrong_post(self):
        response = app.test_client().post('/aggregation?url=jqpd')
        data = response.get_data('error')
        res = json.loads(data)
        self.assertIn('error', res)

    def test_aggregation_empty_post(self):
        response = app.test_client().post('/aggregation?url=')
        data = response.get_data('error')
        res = json.loads(data)
        self.assertIn('error', res)


if __name__ == "__main__":
    unittest.main()
