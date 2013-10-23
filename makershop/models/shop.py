from . import db
from .user import User


shop_admin = db.Table(
    'shop_admin',
    db.Column('shop_id', db.Integer, db.ForeignKey('shop.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
)


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    owner = db.Column(db.Integer, db.ForeignKey(User.id))

    products = db.relationship(
        'Product',
        backref='shop',
        uselist=True,
        lazy='dynamic',
    )

    admins = db.relationship(
        'User',
        secondary=shop_admin,
        backref=db.backref('shops', lazy='dynamic')
    )

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

    def __repr__(self):
        return '<Shop({id}: "{name}")>'.format(id=self.id, name=self.name)