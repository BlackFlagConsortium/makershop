from http import client as http

from flask import Blueprint, redirect, request, session

from ..models.product import Product
from ..models.shop import Shop
from ..models import db
from ..views.common import ApiResponse, ApiRedirectResponse

bp = Blueprint('shop', __name__)


@bp.route('/create/', methods=['POST', ])
def create():
    name = request.form.get('name')
    if not name:
        return ApiResponse('"name" is required.', http.BAD_REQUEST)
    shop = Shop(name=name, owner=session.get('user'))
    db.session.add(shop)
    db.session.commit()

    return ApiResponse(
        {
            'message': 'Shop created',
            'id': shop.id,
        }
    )


@bp.route('/<int:shop_id>/', methods=['GET', ])
def view(shop_id):
    shop = Shop.query.filter_by(id=shop_id).one()
    return ApiResponse(
        {
            'id': shop.id,
            'name': shop.name,
        }
    )


@bp.route('/<int:shop_id>/product/', methods=['POST', ])
def add_product(shop_id):
    title = request.form.get('title')
    if not title:
        return ApiResponse('"title" is required.', http.BAD_REQUEST)
    product = Product(
        shop_id=shop_id,
        title=title,
        description=request.form.get('description'),
        base_price=request.form.get('base_price'),
    )
    db.session.add(product)
    db.session.commit()

    return ApiRedirectResponse(
        location=product.url,
        status=http.CREATED,
        data=product.to_dict(),
    )

@bp.route('/<int:shop_id>/product/<int:product_id>/', methods=['GET', ])
def view_product(shop_id):
    return ''