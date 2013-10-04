from http import client as http

from makershop.models import db
from makershop.models.user import User
from tests import MakershopTestCase


class AuthTestCase(MakershopTestCase):

    def test_password_match(self):
        with self.app.test_request_context():
            user = User(name='Test User', email='test@user.com', password='foo')
            db.session.add(user)
            db.session.commit()

            self.assertTrue(user.check_password('foo'))

    def test_password_mismatch(self):
        with self.app.test_request_context():
            user = User(name='Test User', email='test@user.com', password='foo')
            db.session.add(user)
            db.session.commit()

            self.assertFalse(user.check_password('bar'))


class LoginTestCase(MakershopTestCase):
    def setUp(self):
        super(LoginTestCase, self).setUp()
        self.client = self.app.test_client()

    def test_auth_failed(self):
        r = self.client.post(
            '/user/login/',
            data={
                'username': 'One does not simply',
                'password': 'enter Mordor',
            }
        )

        self.assertApiError(
            response=r,
            status_code=http.FORBIDDEN,
            message='Login failed.'
        )