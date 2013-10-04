from .. import db
from .common import UOM


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String())
    base_price = db.Column(db.Integer, nullable=False)

    def __init__(self):
        pass

    def __repr__(self):
        return '<Product({})>'.format(self.id)


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    unit_of_measure = db.Enum(UOM)