from flask import request
from flask_restplus import Resource
from app.main.util.decorator import token_required
from app.main.business.user_business import UserBusiness
from ..util.dto import UserDto

api = UserDto.api
verify_password_pin = UserDto.verify_password_pin
reset_password = UserDto.reset_password
update_profile = UserDto.update_profile


@api.route('/reset_password')
class ResetPassword(Resource):
    @api.expect(reset_password)
    def post(self):
        """Forgot password"""
        data = request.json
        return UserBusiness.reset_password(data=data)


@api.route('/verify_password_pin')
class VerifyPasswordPin(Resource):
    @api.expect(verify_password_pin)
    def post(self):
        """Verify PIN and change password"""
        data = request.json
        return UserBusiness.verify_password_pin(data=data)


@api.route('/update_profile')
class UpdateProfile(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(update_profile)
    def put(self):
        """Capture user information"""
        auth_header = request.headers.get('authorization')
        data = request.json
        return UserBusiness.update_profile(auth_token=auth_header,data=data)


@api.route('/get_profile')
class GetProfile(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    def get(self):
        """Get user information"""
        auth_header = request.headers.get('authorization')
        return UserBusiness.get_profile(auth_token=auth_header)