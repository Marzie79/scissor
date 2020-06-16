import json
import unittest
from app import app

app.testing = True


class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_url_first(self):
        response = app.test_client().post(
            '/?url=http://adshjkl.ir'
        )
        data = response.get_data('url')
        res = json.loads(data)
        self.assertIn('short_url', res)

    def test_url_second(self):
        response = app.test_client().post(
            '/?url=http://'
        )
        data = response.get_data('url')
        res = json.loads(data)
        self.assertIn('error', res)

    def test_url_third(self):
        response = app.test_client().post(
            '/?url=http://k.com'
        )
        data = response.get_data('url')
        res = json.loads(data)
        self.assertIn('short_url', res)

    def test_url_forth(self):
        response = app.test_client().post(
            '/?url=http://.com'
        )
        data = response.get_data('url')
        res = json.loads(data)
        self.assertIn('error', res)


if __name__ == "__main__":
    unittest.main()
