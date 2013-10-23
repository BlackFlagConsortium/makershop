import pprint
import unittest

from flask import json

from makershop import create_app
from makershop.models import db
from .factories import UserFactory


class MakershopTestCase(unittest.TestCase):
    def setUp(self):
        #db.create_all(app=create_app())
        self.app = create_app()
        self.app.debug = True
        #self.client = self.app.test_client()
        with self.app.test_request_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.test_request_context():
            db.drop_all()

    def assert_api_error(self, response, status_code, message):
        if response.status_code != status_code:
            raise AssertionError(
                "HTTP Status: {actual} !== {expected}".format(
                    actual=response.status_code,
                    expected=status_code,
                )
            )

        if json.loads(response.data) != {'message': message}:
                raise AssertionError(
                    'returned JSON:\n\nGot: {}\n\nExpected: {}'.format(
                        response.data.decode('utf-8'),
                        json.dumps({'message': message})
                    )
                )


class UserLoggedIn(MakershopTestCase):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()

        with self.app.test_request_context():
            self.user = UserFactory.create(password='foo')

            self.client.post(
                '/user/login/',
                data={
                    'username': self.user.email,
                    'password': 'foo',
                }
            )
