from flask_restplus import Resource
from app.main.util.decorator import token_required
from app.main.business.app_business import AppBusiness
from flask import request
from ..util.dto import AppDto
api = AppDto.api
update_whole_app = AppDto.update_whole_app


@api.route('/update_whole_app')
class UpdateWholeApp(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(update_whole_app)
    def post(self):
        """Update whole app"""
        auth_header = request.headers.get('authorization')
        data = request.json
        return AppBusiness.update_whole_app(auth_token=auth_header,data=data)