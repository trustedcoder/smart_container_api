from app.main.helper.auth_methods import AuthMethod
import datetime
from google.oauth2 import id_token
from google.auth.transport import requests
from facebook import GraphAPI
from app.main import db
from app.main.model.users import User
from app.main.helper.user_method import UserMethod
import os


class Auth:
    @staticmethod
    def google_sign_in(data):
        me = id_token.verify_oauth2_token(data['access_token'], requests.Request(), os.getenv('GOOGLE_CLIENT'))
        if 'error_description' not in me:
            if me['aud'] in [os.getenv('GOOGLE_CLIENT')]:
                # check if google id exist in database
                response1 = AuthMethod.is_google_id_exist(me['sub'])
                if response1['status'] == 1:
                    found_user = User.query.filter_by(google_id=me['sub']).first()
                    if found_user:
                        auth_response = found_user.encode_auth_token(found_user.id)
                        if auth_response['status'] == 1:
                            is_profiled = True
                            if found_user.email is None or found_user.fullname is None:
                                is_profiled = False
                            response_object = {
                                'status': 1,
                                'is_profiled': is_profiled,
                                'email': found_user.email,
                                'name': str(found_user.fullname),
                                'message': 'Successfully logged in.',
                                'authorization': auth_response['token'].decode()
                            }
                            return response_object
                        else:
                            response_object = {
                                'status': 0,
                                'message': auth_response['message']
                            }
                            return response_object
                    else:
                        response_object = {
                            'status': 0,
                            'message': 'User not found.'
                        }
                        return response_object
                else:
                    public_id = ('\n'.join(map(str, AuthMethod.random_number(1, 2, 1000000000000))))
                    user_email = me['email'] if 'email' in me else ""
                    response1 = UserMethod.is_email_exist(user_email)
                    if response1['status'] == 1:
                        found_old_user = User.query.filter(User.email == user_email).first()
                        found_old_user.google_id = me['sub']
                        try:
                            db.session.commit()
                            auth_responsea = found_old_user.encode_auth_token(found_old_user.id)
                            if auth_responsea['status'] == 1:
                                response_object = {
                                    'status': 1,
                                    'is_profiled': True if 'email' in me else False,
                                    'email': found_old_user.email,
                                    'name': str(found_old_user.fullname),
                                    'message': 'Successfully logged in.',
                                    'authorization': auth_responsea['token'].decode()
                                }
                                return response_object
                            else:
                                response_object = {
                                    'status': 0,
                                    'message': auth_responsea['message']
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
                        new_user = User(
                            public_id=public_id,
                            google_id=me['sub'],
                            email=me['email'] if 'email' in me else "",
                            is_email_verified=True if 'email' in me else False,
                            fullname=me['name'],
                            date_created=datetime.datetime.now()
                        )
                        AuthMethod.save_changes(new_user)
                    # login user
                    found_user = User.query.filter_by(google_id=me['sub']).first()
                    if found_user:
                        auth_response = found_user.encode_auth_token(found_user.id)
                        if auth_response['status'] == 1:
                            response_object = {
                                'status': 1,
                                'is_profiled': True if 'email' in me else False,
                                'email': found_user.email,
                                'name': str(found_user.fullname),
                                'message': 'Successfully logged in.',
                                'authorization': auth_response['token'].decode()
                            }
                            return response_object
                        else:
                            response_object = {
                                'status': 0,
                                'message': auth_response['message']
                            }
                            return response_object
                    else:
                        response_object = {
                            'status': 0,
                            'message': 'User not found.'
                        }
                        return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'Could not verify audience'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': me['error_description']
            }
            return response_object

    @staticmethod
    def facebook_sign_in(data):
        graph = GraphAPI(data['access_token'])
        me = graph.get_object(id='me', fields='email,name,id,picture.width(100).height(100)')
        if 'error' not in me:
            response1 = AuthMethod.is_facebook_id_exist(me['id'])
            if response1['status'] == 1:
                found_user = User.query.filter_by(facebook_id=me['id']).first()
                if found_user:
                    auth_response = found_user.encode_auth_token(found_user.id)
                    if auth_response['status'] == 1:
                        is_profiled = True
                        if found_user.email is None or found_user.fullname is None:
                            is_profiled = False
                        response_object = {
                            'status': 1,
                            'is_profiled': is_profiled,
                            'email': found_user.email,
                            'name': str(found_user.fullname) ,
                            'message': 'Successfully logged in.',
                            'authorization': auth_response['token'].decode()
                        }
                        return response_object
                    else:
                        response_object = {
                            'status': 0,
                            'message': auth_response['message']
                        }
                        return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'User not found.'
                    }
                    return response_object
            else:
                public_id = ('\n'.join(map(str, AuthMethod.random_number(1, 2, 1000000000000))))
                user_email = me['email'] if 'email' in me else ""
                response1 = UserMethod.is_email_exist(user_email)
                if response1['status'] == 1:
                    found_old_user = User.query.filter(User.email == user_email).first()
                    found_old_user.facebook_id = me['id']
                    try:
                        db.session.commit()
                        auth_responsea = found_old_user.encode_auth_token(found_old_user.id)
                        if auth_responsea['status'] == 1:
                            response_object = {
                                'status': 1,
                                'is_profiled': True if 'email' in me else False,
                                'email': found_old_user.email,
                                'name': str(found_old_user.fullname),
                                'message': 'Successfully logged in.',
                                'authorization': auth_responsea['token'].decode()
                            }
                            return response_object
                        else:
                            response_object = {
                                'status': 0,
                                'message': auth_responsea['message']
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
                    new_user = User(
                        public_id=public_id,
                        facebook_id=me['id'],
                        email=me['email'] if 'email' in me else "",
                        is_email_verified=True if 'email' in me else False,
                        fullname=me['name'],
                        date_created=datetime.datetime.now()
                    )
                    AuthMethod.save_changes(new_user)
                found_user = User.query.filter_by(facebook_id=me['id']).first()
                if found_user:
                    auth_response = found_user.encode_auth_token(found_user.id)
                    if auth_response['status'] == 1:
                        response_object = {
                            'status': 1,
                            'is_profiled': True if 'email' in me else False,
                            'email': found_user.email,
                            'name': str(found_user.fullname),
                            'message': 'Successfully logged in.',
                            'authorization': auth_response['token'].decode()
                        }
                        return response_object
                    else:
                        response_object = {
                            'status': 0,
                            'message': auth_response['message']
                        }
                        return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'User not found.'
                    }
                    return response_object
        else:
            response_object = {
                'status': 0,
                'message': me['error']['message']
            }
            return response_object

    @staticmethod
    def email_register(data):
        # Check if email already exist in database
        email_exist = UserMethod.is_email_exist(data['email'])
        if email_exist:
            # email already exist, do not create account
            response_object = {
                'status': 0,
                'message': 'Email Already exist'
            }
            return response_object
        else:
            # everything is set, create new merchant
            public_id = ('\n'.join(map(str, AuthMethod.random_number(1, 2, 1000000000000))))
            new_user = User(
                password=User.generate_password(data['password']),
                public_id=public_id,
                email=data['email'],
                fullname=data['fullname'],
                is_email_verified = False,
                date_created=datetime.datetime.now()
            )
            AuthMethod.save_changes(new_user)
            response_object = {
                'status': 1,
                'message': 'Account created successfully. Please login  to continue'
            }
            return response_object

    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter(User.email == data['email']).first()
            if user and User.check_password(user.password, data['password']):
                response1 = user.encode_auth_token(user.id)
                if response1['status'] == 1:
                    is_profiled = True
                    if user.email is None or user.fullname is None:
                        is_profiled = False
                    response_object = {
                        'status': 1,
                        'is_profiled': is_profiled,
                        'email': user.email,
                        'name': str(user.fullname),
                        'message': 'Successfully logged in.',
                        'authorization': response1['token'].decode()
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': response1['message']
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'Invalid Details.'
                }
                return response_object
        except Exception as e:
            response_object = {
                'status': 0,
                'message': 'An error occurred. Try again ' + str(e)
            }
            return response_object

    @staticmethod
    def update_profile(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                user = User.query.filter(User.id == resp['user_id']).first()
                user.fullname = data['fullname']

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
    def logout_user(auth_token):
        db.session.rollback()
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                # mark the token as blacklisted
                return AuthMethod.save_token(token=auth_token, expire_date=resp['expire_date'])
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Provide a valid auth token.'
            }
            return response_object