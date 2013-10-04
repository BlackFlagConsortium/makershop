from makershop.models import db
from makershop.models.user import User
from makershop.tests import MakershopTestCase


class StuffTests(MakershopTestCase):

    def test_shop_user(self):
        with self.app.test_request_context():
            user = User(
                email='lyndsy@lyndsysimon.com',
                password='password',
                name='Lyndsy'
            )
            db.session.add(user)
            db.session.commit()

            self.assertEqual(1, len(list(user.emails)))
            self.assertEqual(
                'lyndsy@lyndsysimon.com',
                user.emails[0].email,
            )