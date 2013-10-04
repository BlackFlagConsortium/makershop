from http import client as http

from flask import Blueprint, request
from sqlalchemy.orm.exc import NoResultFound

from .common import ApiResponse

from ..models.user import User

bp = Blueprint('users', __name__)

@bp.route('/login/', methods=['POST', ])
def login():
    u, p = request.form.get('username'), request.form.get('password')
    if not u:
        return ApiResponse('"username" is required', status=http.BAD_REQUEST)
    if not p:
        return ApiResponse('"password" is required', status=http.BAD_REQUEST)

    try:
        if User.find_by_email(u).check_password(p):
            return ApiResponse('Login successful.')
    except NoResultFound:
        # User doesn't exist
        pass

    # if the user doesn't exist -or- if the password is wrong.
    return ApiResponse('Login failed.', status=http.FORBIDDEN)

