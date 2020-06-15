import json
import flask
import unittest

import requests

from app import app

app.testing = True


class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_add(self):
        response = app.test_client().post(
            '/?url=http://adshjkl.ki'
        )
        data = response.get_data('url')
        res = json.loads(data)
        if 'short_url' in res:
            self.assertEqual(res['short_url'], res['short_url'])
        else:
            self.assertEqual('wrong test', res['short_url'])


if __name__ == "__main__":
    unittest.main()
