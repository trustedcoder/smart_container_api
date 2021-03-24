from flask_restplus import Api
from flask import Blueprint
from .main.endpoint.auth_endpoints import api as auth_ns
from .main.endpoint.app_endpoint import api as app_ns
from .main.endpoint.user_endpoint import api as user_ns
from .main.endpoint.container_endpoint import api as container_ns
from .main.endpoint.notify_endpoint import api as notify_ns
from .main.endpoint.shop_endpoint import api as shop_ns
from .main.endpoint.meal_endpoint import api as meal_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Smart Container Api',
          version='1.0',
          description='Get notified when items inside your container are '
                      'about to get exhausted or are completely empty'
          )
api.add_namespace(auth_ns)
api.add_namespace(app_ns)
api.add_namespace(user_ns)
api.add_namespace(container_ns)
api.add_namespace(notify_ns)
api.add_namespace(shop_ns)
api.add_namespace(meal_ns)
