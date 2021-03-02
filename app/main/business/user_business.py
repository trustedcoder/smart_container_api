from app.main import db
from app.main.helper.email_method import EmailMethod
from app.main.helper.auth_methods import AuthMethod
from app.main.model.reset_password import ResetPassword
from app.main.model.users import User
import datetime


class UserBusiness:
    @staticmethod
    def update_profile(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                user = User.query.filter(User.id == resp['user_id']).first()
                user.name = data['name']

                if (user.email is None) or (user.email == ""):
                    user.email = data['email']
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
                response_object = {
                    'status': 1,
                    'message': 'Profile updated'
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
    def get_profile(auth_token):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                user = User.query.filter(User.id == resp['user_id']).first()
                if user:
                    response_object = {
                        'status': 1,
                        'name': str(user.fullname),
                        'email': str(user.email),
                        'message': 'Profile found'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'User profile not found. Please contact support.'
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
    def reset_password(data):
        found_user = User.query.filter(User.email == data['email']).first()
        if found_user:
            public_id = ('\n'.join(map(str, AuthMethod.random_number(1, 2, 1000000))))
            new_pin = ResetPassword(
                pin=public_id,
                user_id=found_user.id
            )
            AuthMethod.save_changes(new_pin)
            EmailMethod.send_reset_password(found_user.fullname, found_user.email, public_id)
            response_object = {
                'status': 1,
                'message': 'Reset PIN sent to your email address. Check your spam folder if not found in inbox.'
            }
            return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Email not found'
            }
            return response_object

    @staticmethod
    def verify_password_pin(data):
        found_pin = ResetPassword.query.filter(ResetPassword.pin == data['pin'],ResetPassword.expire_created > datetime.datetime.now(),ResetPassword.access == True).first()
        if found_pin:
            found_pin.access = False
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            found_user = User.query.filter(User.id == found_pin.user_id).first()
            found_user.password = User.generate_password(data['password'])
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            response_object = {
                'status': 1,
                'message': 'Your password was changed successfully.'
            }
            return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'PIN expired.'
            }
            return response_object
