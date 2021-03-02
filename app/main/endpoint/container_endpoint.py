from flask_restplus import Resource
from app.main.util.decorator import token_required
from app.main.business.container_business import ContainerBusiness
from flask import request
from ..util.req_parser import detect_object,add_container_two
from ..util.dto import ContainerDto
api = ContainerDto.api
add_container_one = ContainerDto.add_container_one
update_weight_level = ContainerDto.update_weight_level
calibrate = ContainerDto.calibrate


@api.route('/add_container_one')
class AddContainerOne(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(add_container_one)
    def patch(self):
        """Add first container details"""
        auth_header = request.headers.get('authorization')
        data = request.json
        return ContainerBusiness.add_container_one(auth_token=auth_header,data=data)


@api.route('/detect_object')
class DetectObject(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(detect_object)
    def patch(self):
        """Detect object"""
        auth_header = request.headers.get('authorization')
        data = detect_object.parse_args(request)
        return ContainerBusiness.detect_object(auth_token=auth_header,data=data)


@api.route('/add_container_two')
class AddContainerTwo(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(add_container_two)
    def patch(self):
        """Save item name and start adding item in the container"""
        auth_header = request.headers.get('authorization')
        data = add_container_two.parse_args(request)
        return ContainerBusiness.add_container_two(auth_token=auth_header,data=data)


@api.route('/update_weight_level')
class UpdateWeightLevel(Resource):
    @api.expect(update_weight_level)
    def post(self):
        """update current weight and level of container"""
        data = request.json
        return ContainerBusiness.update_weight_level(data=data)


@api.route('/calibrate')
class Calibrate(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(calibrate)
    def post(self):
        """calibrate container"""
        auth_header = request.headers.get('authorization')
        data = request.json
        return ContainerBusiness.calibrate(auth_token=auth_header,data=data)


@api.route('/get_containers')
class GetContainer(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    def get(self):
        """get all container for a user"""
        auth_header = request.headers.get('authorization')
        return ContainerBusiness.get_containers(auth_token=auth_header)