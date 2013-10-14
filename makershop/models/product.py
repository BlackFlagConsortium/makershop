from flask import json, url_for

from . import db
from .common import UOM
from .shop import Shop


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey(Shop.id))
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String())
    base_price = db.Column(db.Integer)
    visible = db.Column(db.Boolean, default=False)

    def __init__(self, shop_id, title, description=None, base_price=None,
                 visible=False):

        # If shop isn't a `Shop` object, assume it's an ID
        self.shop_id = shop_id
        self.title = title
        self.description = description or self.description
        self.base_price = base_price or self.base_price
        self.visible = visible or self.visible

    def __repr__(self):
        return '<Product({})>'.format(self.id)

    @property
    def url(self):
        return url_for(
            'shop.view_product',
            shop_id=self.shop_id,
            product_id=self.id
        )

    def to_dict(self):
        return {
            'id': self.id,
            'shop_id': self.shop_id,
            'title': self.title,
            'description': self.description,
            'base_price': self.base_price,
            'visible': self.visible,
        }


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    unit_of_measure = db.Enum(UOM)