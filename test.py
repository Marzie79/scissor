import json
import unittest
from app import app

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


if __name__ == "__main__":
    unittest.main()
