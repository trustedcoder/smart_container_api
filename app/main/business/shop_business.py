from app.main.helper.container_methods import ContainerMethod
from ..model.containers import Containers
from app.main.model.users import User
from ..model.shopping import Shopping
from app.main import db


class ShopBusiness:
    @staticmethod
    def get_shopping_list(auth_token):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                shoppings = Shopping.query.join(Containers, Containers.id == Shopping.container_id).filter(Containers.user_id == resp['user_id']).all()
                if shoppings:
                    list_shopping = []
                    for shopping in shoppings:
                        container =  Containers.query.filter(Containers.id == shopping.container_id).first()
                        if container.is_countable:
                            unit = 'kg'
                        else:
                            unit = 'cm'
                        list_shopping.append({
                            'container_id': shopping.container_id,
                            'image': ContainerMethod.get_container_item_image(shopping.container_id),
                            'title': ContainerMethod.get_container_item_name(shopping.container_id),
                            'weight_level_remaining': str(ContainerMethod.get_item_weight_level_remaining(shopping.container_id))+unit,
                            'percent_remaining': "{:.2f}".format(ContainerMethod.get_item_percent_remaining(shopping.container_id)),
                            'is_bought': shopping.is_bought
                        })
                    response_object = {
                        'status': 1,
                        'data': list_shopping,
                        'message': 'shopping lists found'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 1,
                        'data': [],
                        'message': 'No shopping lists found'
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
    def set_bought(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                shopping = Shopping.query.join(Containers, Containers.id == Shopping.container_id).filter(
                    Containers.user_id == resp['user_id'], Shopping.container_id == data['container_id']).first()
                if shopping:
                    shopping.is_bought = data['is_bought']
                    try:
                        db.session.commit()
                        response_object = {
                            'status': 1,
                            'message': 'Changes saved'
                        }
                        return response_object
                    except Exception as e:
                        db.session.rollback()
                        response_object = {
                            'status': 0,
                            'message': str(e)
                        }
                        return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'Item not found in shopping list.'
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
