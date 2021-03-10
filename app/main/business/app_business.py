from app.main.helper.user_method import UserMethod
from ..helper.notify_methods import NotifyMethod
from app.main.model.users import User
from app.main import db


class AppBusiness:
    @staticmethod
    def update_whole_app(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                response = User.query.filter(User.id == resp['user_id']).first()
                if response:
                    response.fcm_token = data['fcm_token']
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                        raise
                    response_object = {
                        'status': 1,
                        'total_notify': NotifyMethod.get_notify_total(resp['user_id']),
                        'fullname': UserMethod.get_fullname(resp['user_id']),
                        'email': UserMethod.get_email(resp['user_id']),
                        'message': 'Token updated successfully.'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'User not found'
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
