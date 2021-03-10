from flask_restplus import Resource
from app.main.util.decorator import token_required
from app.main.business.notify_business import NotifyBusiness
from flask import request
from ..util.req_parser import get_containers
from ..util.dto import NotifyDto
api = NotifyDto.api


@api.route('/get_notifications')
class GetNotifications(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(get_containers)
    def get(self):
        """Get all notifications"""
        auth_header = request.headers.get('authorization')
        data = get_containers.parse_args(request)
        return NotifyBusiness.get_notifications(auth_token=auth_header,data=data)