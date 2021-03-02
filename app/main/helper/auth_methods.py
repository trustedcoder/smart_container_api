from app.main import db
from app.main.model.users import User
from app.main.model.blacklist import BlacklistToken
import random


class AuthMethod:
    @staticmethod
    def is_google_id_exist(google_id):
        found = User.query.filter_by(google_id=google_id).first()
        if found:
            response_object = {
                'status': 1,
                'message': 'User Google ID found.',
            }
            return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'User Google ID not found.',
            }
            return response_object

    @staticmethod
    def is_facebook_id_exist(facebook_id):
        found = User.query.filter_by(facebook_id=facebook_id).first()
        if found:
            response_object = {
                'status': 1,
                'message': 'User facebook ID found.',
            }
            return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'User facebook ID not found.',
            }
            return response_object

    @staticmethod
    def save_changes(data):
        try:
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    @staticmethod
    def random_number(count, start, stop, step=1):
        def gen_random():
            while True:
                yield random.randrange(start, stop, step)

        def gen_n_unique(source, n):
            seen = set()
            seenadd = seen.add
            for i in (i for i in source() if i not in seen and not seenadd(i)):
                yield i
                if len(seen) == n:
                    break

        return [i for i in gen_n_unique(gen_random, min(count, int(abs(stop - start) / abs(step))))]

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                user = User.query.filter_by(id=resp['user_id']).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'registered_on': str(user.date_created)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 0,
                'message': resp['message']
            }
            return response_object, 401
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object, 401

    @staticmethod
    def save_token(token,expire_date):
        db.session.rollback()
        blacklist_token = BlacklistToken(token=token, expire_date=expire_date)
        try:
            # insert the token
            try:
                db.session.add(blacklist_token)
                db.session.commit()
            except:
                db.session.rollback()
                raise
            response_object = {
                'status': 1,
                'message': 'Successfully logged out.'
            }
            return response_object
        except Exception as e:
            response_object = {
                'status': 0,
                'message': 'Error'
            }
            return response_object

    @staticmethod
    def get_social_image(image):
        if image == "":
            return "https://res.cloudinary.com/howla/image/upload/v1603528008/profile_image/no_profile_lqscrk.png"
        else:
            return image