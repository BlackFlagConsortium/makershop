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

    def test_auth_failure_user_not_found(self):
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

    def test_auth_failure_bad_password(self):
        with self.app.test_request_context():
            u = User(email='foo@bar.com', password='correct password')
            db.session.add(u)
            db.session.commit()

        r = self.client.post(
            '/user/login/',
            data={
                'username': 'foo@bar.com',
                'password': 'incorrect password',
            }
        )

        self.assertApiError(
            response=r,
            status_code=http.FORBIDDEN,
            message='Login failed.'
        )

    def test_auth_success(self):
        with self.app.test_request_context():
            u = User(email='foo@bar.com', password='asdfasdf')
            db.session.add(u)
            db.session.commit()

        r = self.client.post(
            '/user/login/',
            data={
                'username': 'foo@bar.com',
                'password': 'asdfasdf',
            }
        )

        self.assertEqual(http.OK, r.status_code)


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

        self.assertApiError(
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

        self.assertApiError(
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

        self.assertApiError(
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

        self.assertEqual(http.OK, r.status_code)
