import pprint
import unittest

from flask import json

from makershop import create_app
from makershop.models import db


class MakershopTestCase(unittest.TestCase):
    def setUp(self):
        #db.create_all(app=create_app())
        self.app = create_app()
        self.app.debug = True
        #self.client = self.app.test_client()
        with self.app.test_request_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.test_request_context():
            db.drop_all()

    def assertApiError(self, response, status_code, message):
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