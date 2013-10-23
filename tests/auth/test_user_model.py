from nose.tools import *

from .. import MakershopTestCase
from ..factories import UserFactory


class AuthTestCase(MakershopTestCase):

    def test_password_match(self):
        with self.app.test_request_context():
            user = UserFactory.create(password='foo')

            assert_true(user.check_password('foo'))

    def test_password_mismatch(self):
        with self.app.test_request_context():
            user = UserFactory.create(password='foo')

            assert_false(user.check_password('bar'))