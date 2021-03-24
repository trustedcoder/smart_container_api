from flask_restplus import Resource
from app.main.util.decorator import token_required
from app.main.business.meal_business import MealBusiness
from flask import request
from ..util.dto import MealDto
from ..util.req_parser import new_meal_save,get_all_ingredient,suggest_meal_list
api = MealDto.api
remove_add_ingredient = MealDto.remove_add_ingredient


@api.route('/get_meal_list')
class MealList(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    def get(self):
        """get meal list"""
        auth_header = request.headers.get('authorization')
        return MealBusiness.get_meal_list(auth_token=auth_header)


@api.route('/new_meal_save')
class NewMealSave(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(new_meal_save)
    def post(self):
        """Save new meal"""
        auth_header = request.headers.get('authorization')
        data = new_meal_save.parse_args(request)
        return MealBusiness.new_meal_save(auth_token=auth_header,data=data)


@api.route('/get_all_ingredient')
class MealIngredientsList(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(get_all_ingredient)
    def get(self):
        """get meal list ingredients"""
        auth_header = request.headers.get('authorization')
        data = get_all_ingredient.parse_args(request)
        return MealBusiness.get_all_ingredient(auth_token=auth_header,data=data)


@api.route('/remove_add_ingredient')
class RemoveAddIngredient(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(remove_add_ingredient)
    def post(self):
        """Remove or add meal"""
        auth_header = request.headers.get('authorization')
        data = request.json
        return MealBusiness.new_meal_save(auth_token=auth_header,data=data)


@api.route('/suggest_meal_list')
class SuggestMeal(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(suggest_meal_list)
    def get(self):
        """suggest meals"""
        auth_header = request.headers.get('authorization')
        data = suggest_meal_list.parse_args(request)
        return MealBusiness.suggest_meal_list(auth_token=auth_header,data=data)