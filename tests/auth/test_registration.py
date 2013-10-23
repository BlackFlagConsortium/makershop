from http import client as http

from nose.tools import *

from makershop.models import db
from makershop.models.user import User
from tests import MakershopTestCase


class RegistrationTestCase(MakershopTestCase):
    def setUp(self):
        super(RegistrationTestCase, self).setUp()
        self.client = self.app.test_client()

    def test_registration_no_email(self):
        r = self.client.post(
            '/user/register/',
            data={
                'password': 'asdfasdf',
                'name': 'Test User',
            }
        )

        self.assert_api_error(
            response=r,
            status_code=http.BAD_REQUEST,
            message='"email" is required.'
        )

    def test_registration_no_password(self):
        r = self.client.post(
            '/user/register/',
            data={
                'email': 'foo@bar.com',
                'name': 'Test User',
            }
        )

        self.assert_api_error(
            response=r,
            status_code=http.BAD_REQUEST,
            message='"password" is required.'
        )

    def test_registration_duplicate_email(self):
        with self.app.test_request_context():
            u = User(email='foo@bar.com', password='asdfasdf')
            db.session.add(u)
            db.session.commit()

        r = self.client.post(
            '/user/register/',
            data={
                'email': 'foo@bar.com',
                'password': 'asdfasdf',
                'name': 'Test User',
            }
        )

        self.assert_api_error(
            response=r,
            status_code=http.BAD_REQUEST,
            message='Email associated with existing account.'
        )

    def test_registration_success(self):
        r = self.client.post(
            '/user/register/',
            data={
                'email': 'foo@bar.com',
                'password': 'asdfasdf',
                'name': 'Test User',
            }
        )

        assert_equal(http.OK, r.status_code)