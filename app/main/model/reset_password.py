from .. import db
import datetime
from app.main.model.users import User


class ResetPassword(db.Model):
    """
    ResetPassword Model for storing school class
    """
    __tablename__ = 'reset_password'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pin = db.Column(db.String(255),unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    expire_created = db.Column(db.DateTime, nullable=False)
    access = db.Column(db.Boolean,nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now())

    def __init__(self,pin,user_id):
        self.pin = pin
        self.user_id = user_id
        self.access = True
        self.expire_created = datetime.datetime.now() + datetime.timedelta(hours=24)
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return self.pin