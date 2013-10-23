from http import client as http

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

    def test_logout(self):
        r = self.client.post('/user/logout/')

        assert_equal(http.OK, r.status_code)