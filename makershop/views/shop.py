from http import client as http

from flask import Blueprint, request

from ..models.shop import Shop
from ..models import db
from ..views.common import ApiResponse

bp = Blueprint('shop', __name__)


@bp.route('/create/', methods=['POST', ])
def create():
    name = request.form.get('name')
    if not name:
        return ApiResponse('"name" is required.', http.BAD_REQUEST)
    shop = Shop(name=name)
    db.session.add(shop)
    db.session.commit()

    return ApiResponse(
        {
            'message': 'Shop created',
            'id': shop.id,
        }
    )