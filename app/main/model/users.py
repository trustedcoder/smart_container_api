from .. import db,flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

roles_users_table = db.Table('roles_users',
      db.Column('users_id', db.Integer(),
      db.ForeignKey('users.id')),
      db.Column('roles_id', db.Integer(),
      db.ForeignKey('roles.id')))


class Roles(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(225), unique=True, nullable=False)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=True)
    fullname = db.Column(db.String(225))
    is_email_verified = db.Column(db.Boolean,nullable=False)
    google_id = db.Column(db.String(255))
    facebook_id = db.Column(db.String(255))
    fcm_token = db.Column(db.String(255))
    date_created = db.Column(db.DateTime)
    roles = db.relationship('Roles', secondary=roles_users_table,backref='user', lazy=True)

    def __repr__(self):
        return "{}".format(self.public_id)

    @staticmethod
    def generate_password(pass_word):
        return flask_bcrypt.generate_password_hash(pass_word).decode('utf-8')

    @staticmethod
    def check_password(password, pass_word):
        return flask_bcrypt.check_password_hash(password, pass_word)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10950, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            auth_token = jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
            response_object = {
                'status': 1,
                'message': 'Authorization Token generated successfully',
                'token': auth_token,
            }
            return response_object
        except Exception as e:
            response_object = {
                'status': 0,
                'message': 'An error occurred. Try Again',
            }
            return response_object

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                response_object = {
                    'status': 0,
                    'message': 'Please log in again.',
                }
                return response_object
            else:
                response_object = {
                    'status': 1,
                    'message': 'Authorization Token Decoded successfully',
                    'user_id': payload['sub'],
                    'expire_date': payload['exp'],
                }
                return response_object
        except jwt.ExpiredSignatureError:
            response_object = {
                'status': 0,
                'message': 'Blocked.',
            }
            return response_object
        except jwt.InvalidTokenError:
            response_object = {
                'status': 0,
                'message': 'Blocked.',
            }
            return response_object