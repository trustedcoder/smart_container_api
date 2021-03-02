from app.main import db
from app.main.model.users import User


class UserMethod:
    @staticmethod
    def is_email_exist(email):
        found = User.query.filter(User.email==email).first()
        if found:
            return True
        else:
            return False

    @staticmethod
    def save_changes(data):
        db.session.add(data)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    @staticmethod
    def get_fullname(user_id):
        found = User.query.filter(User.id == user_id).first()
        if found:
            return found.fullname
        else:
            return ''

    @staticmethod
    def get_user_fcm_token(user_id):
        found = User.query.filter(User.id == user_id).first()
        if found:
            return str(found.fcm_token)
        else:
            return ''

    @staticmethod
    def get_email(user_id):
        found = User.query.filter(User.id == user_id).first()
        if found:
            return found.email
        else:
            return ''