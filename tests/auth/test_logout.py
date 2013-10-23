from http import client as http

import flask
from nose.tools import *

from .. import MakershopTestCase
from ..factories import UserFactory


class LogoutTestCase(MakershopTestCase):
    def setUp(self):
        super(LogoutTestCase, self).setUp()
        self.client = self.app.test_client()

        with self.app.test_request_context():
            u = UserFactory.create(password='foo')

            self.client.post(
                '/user/login/',
                data={
                    'username': u.email,
                    'password': 'foo',
                }
            )

    def test_logout_returns_success(self):
        r = self.client.post('/user/logout/')

        assert_equal(http.OK, r.status_code)

    def test_logout_success_session(self):
        with self.app.test_client() as tc:
            with tc.session_transaction() as s:
                s['user_id'] = 1

            tc.post('/user/logout/')

            assert_is_none(flask.session.get('user_id'))

