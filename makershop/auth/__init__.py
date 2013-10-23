from functools import wraps
from http import client as http

from flask import session, abort

from ..views.common import ApiResponse


def auth_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            return ApiResponse(
                'You are not logged in.',
                status=http.UNAUTHORIZED,
            )
        return f(*args, **kwargs)
    return wrapped