from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    social_sign_in = api.model('social_sign_in', {
        'access_token': fields.String(required=True, description='social access token')
    })
    user_login = api.model('user_login', {
        'email': fields.String(required=True, description='Email'),
        'password': fields.String(required=True, description='Password'),
    })
    user_register = api.model('user_register', {
        'fullname': fields.String(required=True, description='fullname'),
        'email': fields.String(required=True, description='Email'),
        'password': fields.String(required=True, description='Password')
    })


class AppDto:
    api = Namespace('app', description='General app related operations')

    update_whole_app = api.model('update_whole_app', {
        'fcm_token': fields.String(required=True, description='FCM token'),
    })


class UserDto:
    api = Namespace('users', description='Users related operations')
    verify_password_pin = api.model('verify_password_pin', {
        'password': fields.String(required=True, description='Password'),
        'pin': fields.String(required=True, description='PIN')
    })

    reset_password = api.model('reset_password', {
        'email': fields.String(required=True, description='Email address'),
    })


class ContainerDto:
    api = Namespace('container', description='Container related operations')
    add_container_one = api.model('add_container_one', {
        'container_id': fields.String(required=True, description='Container ID'),
        'name': fields.String(required=True, description='Container name'),
        'state': fields.String(required=True, description='State of the item'),
        'is_edible': fields.Boolean(required=True, description='Is the item edible'),
    })

    update_weight_level = api.model('update_weight_level', {
        'container_id': fields.String(required=True, description='Container ID'),
        'level': fields.Float(required=True, description='Level in cm of the container'),
        'weight': fields.Float(required=True, description='Weight of the container'),
    })

    calibrate = api.model('calibrate', {
        'container_id': fields.String(required=True, description='Container ID'),
    })

    reset_password = api.model('reset_password', {
        'email': fields.String(required=True, description='Email address'),
    })