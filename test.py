import json
import unittest
from app import app
from flask import url_for

app.testing = True


class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_true_url(self):
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


if __name__ == "__main__":
    unittest.main()
