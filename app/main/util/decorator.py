from functools import wraps
from flask import request

from app.main.helper.auth_methods import AuthMethod


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = AuthMethod.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated