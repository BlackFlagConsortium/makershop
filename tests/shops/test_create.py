from http import client as http

from flask import json
from nose.tools import *

from .. import MakershopTestCase, UserLoggedIn


class NotLoggedIn(MakershopTestCase):
    def test_refused(self):
        with self.app.test_client() as c:
            r = c.post(
                '/shop/create/',
                data={
                    'name': 'Test Shop'
                }
            )

            self.assert_api_error(
                response=r,
                status_code=http.UNAUTHORIZED,
                message='You are not logged in.',
            )


class LoggedIn(UserLoggedIn):
    def test_make_shop(self):

        r = self.client.post(
            '/shop/create/',
            data={
                'name': 'Test Shop'
            }
        )

        assert_equal(http.OK, r.status_code)

        msg = json.loads(r.data)

        assert_is_not_none(msg.get('id'))