from http import client as http

from flask import Blueprint, request, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from .common import ApiResponse

from ..models import db
from ..models.user import User

bp = Blueprint('users', __name__)


@bp.route('/login/', methods=['POST', ])
def login():
    u, p = request.form.get('username'), request.form.get('password')
    if not u:
        return ApiResponse('"username" is required.', status=http.BAD_REQUEST)
    if not p:
        return ApiResponse('"password" is required.', status=http.BAD_REQUEST)

    try:
        user = User.query.filter_by(email=u).one()

        if user.check_password(p):
            session['user_id'] = user.id
            return ApiResponse('Login successful.')
    except NoResultFound:
        # User doesn't exist
        pass

    # if the user doesn't exist -or- if the password is wrong.
    return ApiResponse('Login failed.', status=http.FORBIDDEN)


@bp.route('/logout/', methods=['POST', ])
def logout():
    session['user_id'] = None
    return ApiResponse('Logout successful.')


@bp.route('/register/', methods=['POST', ])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return ApiResponse('"email" is required.', status=http.BAD_REQUEST)
    if not password:
        return ApiResponse('"password" is required.', status=http.BAD_REQUEST)

    try:
        db.session.add(
            User(email=email, password=password, name=request.form.get('name'))
        )
        db.session.commit()
        return ApiResponse('Registration successful.')
    except IntegrityError:
        return ApiResponse(
            'Email associated with existing account.',
            status=http.BAD_REQUEST,
        )
