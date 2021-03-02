from flask import request
from flask_restplus import Resource
from app.main.util.decorator import token_required

from app.main.business.auth_business import Auth
from ..util.dto import AuthDto

api = AuthDto.api
email_register = AuthDto.user_register
email_login = AuthDto.user_login
social_sign_in = AuthDto.social_sign_in


@api.route('/google_sign_in')
class GoogleSignIn(Resource):
    @api.expect(social_sign_in)
    def post(self):
        """Sign in user with google"""
        data = request.json
        return Auth.google_sign_in(data=data)


@api.route('/facebook_sign_in')
class FacebookSignIn(Resource):
    @api.expect(social_sign_in)
    def post(self):
        """Sign in user with facebook"""
        data = request.json
        return Auth.facebook_sign_in(data)


@api.route('/email_register')
class EmailRegister(Resource):
    @api.expect(email_register)
    def post(self):
        """Register new user"""
        data = request.json
        return Auth.email_register(data=data)


@api.route('/email_login')
class EmailLogin(Resource):
    @api.expect(email_login)
    def post(self):
        """Login User"""
        data = request.json
        return Auth.login_user(data=data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @token_required
    @api.doc('logout a user')
    @api.header('authorization', 'JWT TOKEN')
    def post(self):
        # get auth token
        """Logout user"""
        auth_header = request.headers.get('authorization')
        return Auth.logout_user(auth_token=auth_header)