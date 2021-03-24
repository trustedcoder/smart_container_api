import os

from app.main.helper.meal_method import MealMethod
from ..helper.auth_methods import AuthMethod
from ..helper.container_methods import ContainerMethod
from ..model.containers import Containers
from ..model.meal_ingredients import MealsIngredient
from app.main.model.users import User
from ..model.meals import Meals
from app.main import db


class MealBusiness:
    @staticmethod
    def get_meal_list(auth_token):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                meals = Meals.query.filter(Meals.user_id == resp['user_id']).all()
                if meals:
                    list_meal = []
                    for meal in meals:
                        list_meal.append({
                            'meal_id': meal.id,
                            'image': 'static/'+str(meal.image),
                            'name': meal.name,
                            'cook_time': meal.cook_time
                        })
                    response_object = {
                        'status': 1,
                        'data': list_meal,
                        'message': 'meals found'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 0,
                        'data': [],
                        'message': 'No meal found'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def new_meal_save(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                found_meal = Meals.query.filter(Meals.user_id == resp['user_id'], Meals.name == data['name']).first()
                if not found_meal:
                    try:
                        name = ('\n'.join(map(str, AuthMethod.random_number(1, 2, 10000000000000000000000))))
                        real_name = data['image'].filename
                        destination = os.path.join('app/main/static/' + name + '/')
                        if not os.path.exists(destination):
                            os.makedirs(destination)
                        image_file = '%s%s' % (destination, real_name)
                        data['image'].save(image_file)
                        new_meal = Meals(
                            user_id = resp['user_id'],
                            name = data['name'],
                            cook_time= data['cook_time'],
                            image=name + '/' +real_name
                        )

                        db.session.add(new_meal)
                        db.session.commit()
                        find_meal = Meals.query.filter(Meals.user_id == resp['user_id'], Meals.name == data['name'], Meals.cook_time == data['cook_time'], Meals.image == name + '/' +real_name).first()
                        if find_meal:

                            for ingredient in data['ingredient']:
                                ingredient = ingredient.split('|')
                                print(ingredient)
                                new_ingredient = MealsIngredient(
                                    meal_id=find_meal.id,
                                    quantity_one = float(ingredient[1]),
                                    container_id=ingredient[0]
                                )
                                db.session.add(new_ingredient)
                                db.session.commit()
                        response_object = {
                            'status': 1,
                            'message': 'Meal saved.'
                        }
                        return response_object
                    except Exception as e:
                        db.session.rollback()
                        response_object = {
                            'status': 0,
                            'message': 'Meal not saved.'+str(e)
                        }
                        return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'Meal name already created.'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def get_all_ingredient(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                if data.get('meal_id'):
                    meal_id = data['meal_id']
                else:
                    meal_id = 0
                ingredients = Containers.query.filter(Containers.is_edible == True).all()
                if ingredients:
                    list_ingredient = []
                    for ingredient in ingredients:
                        if ingredient.is_countable:
                            unit = 'kg'
                        else:
                            unit = 'cm'
                        list_ingredient.append({
                            'meal_id': meal_id,
                            'container_id': ingredient.id,
                            'image': 'static/'+str(ingredient.image_item),
                            'unit': unit,
                            'name': ingredient.name_item,
                            'is_added': MealMethod.is_found_ingredient(meal_id, ingredient.id)
                        })
                    response_object = {
                        'status': 1,
                        'data': list_ingredient,
                        'message': 'meal ingredients found'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 0,
                        'data': [],
                        'message': 'No meal found'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def remove_add_ingredient(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                if data['is_remove']:
                    try:
                        found_ingredient = MealsIngredient.query.filter(MealsIngredient.meal_id == data['meal_id'], MealsIngredient.container_id == data['container_id'])
                        db.session.delete(found_ingredient)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                else:
                    try:
                        new_ingredient = MealsIngredient(
                            meal_id=data['meal_id'],
                            container_id=data['container_id']
                        )
                        db.session.add(new_ingredient)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                response_object = {
                    'status': 1,
                    'message': 'Changes saved'
                }
                return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def suggest_meal_list(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                meals = Meals.query.filter(Meals.user_id == resp['user_id']).all()
                if meals:
                    list_meal = []
                    for meal in meals:
                        is_add = True
                        meal_ingredients = MealsIngredient.query.filter(MealsIngredient.meal_id == meal.id).all()
                        for ingredient in meal_ingredients:
                            remaining = ContainerMethod.get_item_weight_level_remaining(ingredient.container_id)
                            total_cm_kg = float(data['people_count']*float(ingredient.quantity_one))
                            if remaining < total_cm_kg:
                                is_add = False
                                break
                        if is_add:
                            list_meal.append({
                                'meal_id': meal.id,
                                'image': 'static/'+str(meal.image),
                                'name': meal.name,
                                'people_count': data['people_count'],
                                'cook_time': meal.cook_time
                            })
                    response_object = {
                        'status': 1,
                        'data': list_meal,
                        'message': 'meals found'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 0,
                        'data': [],
                        'message': 'No meal found'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object
