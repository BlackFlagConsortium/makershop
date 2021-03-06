import factory
from factory.alchemy import SQLAlchemyModelFactory

from makershop.models import db
from makershop.models.user import User


class UserFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = User
    FACTORY_SESSION = db.session

    email = factory.Sequence(lambda x: 'john_{}@domain.com'.format(x))
    password = 'fake_password'
    name = factory.Sequence(lambda x: 'John{}'.format(x))

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        rv = super()._create(target_class, *args, **kwargs)
        db.session.commit()
        return rv