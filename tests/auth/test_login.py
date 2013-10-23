from http import client as http

import flask
from nose.tools import *

from .. import MakershopTestCase
from ..factories import UserFactory


class LoginTestCase(MakershopTestCase):
    def setUp(self):
        super(LoginTestCase, self).setUp()
        self.client = self.app.test_client()

    def test_auth_failure_user_not_found(self):
        r = self.client.post(
            '/user/login/',
            data={
                'username': 'One does not simply',
                'password': 'enter Mordor',
            }
        )

        self.assert_api_error(
            response=r,
            status_code=http.FORBIDDEN,
            message='Login failed.'
        )

    def test_auth_failure_bad_password(self):
        with self.app.test_request_context():
            u = UserFactory.create()

            r = self.client.post(
                '/user/login/',
                data={
                    'username': u.email,
                    'password': 'incorrect password',
                }
            )

        self.assert_api_error(
            response=r,
            status_code=http.FORBIDDEN,
            message='Login failed.'
        )

    def test_auth_returns_success(self):
        with self.app.test_request_context():
            u = UserFactory.create(password='foo')

            r = self.client.post(
                '/user/login/',
                data={
                    'username': u.email,
                    'password': 'foo',
                }
            )

        assert_equal(http.OK, r.status_code)

    def test_auth_success_session(self):

        with self.app.test_client() as c:
            with self.app.test_request_context():
                u = UserFactory.create(password='foo')

            r = c.post(
                '/user/login/',
                data={
                    'username': u.email,
                    'password': 'foo',
                }
            )

            assert_equal(u.id, flask.session.get('user_id'))