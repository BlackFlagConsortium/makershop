from . import db
from .user import User


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    owner = db.Column(db.ForeignKey(User))

    def __init__(self, name=None):
        if name:
            self.name = name

    def __repr__(self):
        return '<Shop({id}: "{name}")>'.format(id=self.id, name=self.name)