#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import AddressStops, Address, Stop, User
from config import Config, TestingConfig

from mock import patch

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig())
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan', email='email@email.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

# class AddressModelCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app(TestingConfig(Config))
#         # self.app_context = self.app.app_context()
#         # self.app_context.push()
#         db.create_all()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()

# class StopModelCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app(TestingConfig(Config))
#         # self.app_context = self.app.app_context()
#         # self.app_context.push()
#         db.create_all()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()

# class ArrivalServiceCase(unittest.TestCase):

#       def setUp(self):
#         self.app = create_app(TestingConfig(Config))

#       # def test_get_arrivals(self):
#         # mock external api request
#         # return groomed data if there is some
#         # if no data return None object
#         # test any edge cases or errors?

# class GeoCodingServiceCase(unittest.TestCase):

#       def setUp(self):
#         self.app = create_app(TestingConfig(Config))

#       # def test_get_coordinates(self):
#         # mock external api request
#         # return groomed data if there is some
#         # if no data return None object
#         # test any edge cases or errors?

# class StopServiceCase(unittest.TestCase):

#     def setUp(self):
#         self.app = create_app(TestingConfig())
#         # self.client = self.app.test_client()
#         self.app_context = self.app.app_context()
#         self.app_context.push()

    # def test_get_stops(self):
      # mock external api request
      # return groomed data if there is some
      # if no data return None object
      # test any edge cases or errors?

#     def test_get_stops(self):
#         with patch('requests.get') as mock_request:
#             url = 'http://www.notarealpage.net'

#             # set a `status_code` attribute on the mock object
#             # with value 200
#             mock_request.return_value.status_code = 200

#             self.assertTrue(url_exists(url))

#             # test if requests.get was called
#             # with the given url or not
#             mock_request.assert_called_once_with(url)

#             fake_response = FakeResponse()

# class FakeResponse(object):
#     # default response attributes
#     status_code = 200
#     # response = {
#     #     '@locid'= '3333',
#     #     '@desc' = '123 Muffin Lane',
#     #     '@lat' = '1111'
#     #     '@lng' = '-2222',
#     #     '@dir' = 'downtown'
#     # }
#     content = "Some content"


if __name__ == '__main__':
    unittest.main(verbosity=2)
