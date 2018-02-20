#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Address, Stop
from config import Config, TestingConfig

from mock import patch

# can I call config directly here?
# class TestingConfig(Config):
#     TESTING = True

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig())
        print(self.app.config['SQLALCHEMY_DATABASE_URI'])
        self.client = self.app.test_client()
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

#       def setUp(self):
#         self.app = create_app(TestingConfig(Config))

#       # def test_get_stops(self):
#           # mock external api request
#           # return groomed data if there is some
#           # if no data return None object
#           # test any edge cases or errors?

if __name__ == '__main__':
    unittest.main(verbosity=2)
