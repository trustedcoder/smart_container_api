from flask_restplus import Resource
from app.main.util.decorator import token_required
from app.main.business.shop_business import ShopBusiness
from flask import request
from ..util.dto import ShoppingDto
api = ShoppingDto.api
set_bought = ShoppingDto.set_bought


@api.route('/get_shopping_list')
class ShoppingList(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    def get(self):
        """get shopping list"""
        auth_header = request.headers.get('authorization')
        return ShopBusiness.get_shopping_list(auth_token=auth_header)


@api.route('/set_bought')
class SetBought(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(set_bought)
    def post(self):
        """Set item bought"""
        auth_header = request.headers.get('authorization')
        data = request.json
        return ShopBusiness.set_bought(auth_token=auth_header,data=data)