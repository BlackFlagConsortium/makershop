from http import client as http

import flask
from nose.tools import *

from makershop.models import db
from makershop.models.user import User
from tests import MakershopTestCase
from tests.factories import UserFactory


class AuthTestCase(MakershopTestCase):

    def test_password_match(self):
        with self.app.test_request_context():
            user = UserFactory.create(password='foo')

            assert_true(user.check_password('foo'))

    def test_password_mismatch(self):
        with self.app.test_request_context():
            user = UserFactory.create(password='foo')

            assert_false(user.check_password('bar'))


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
