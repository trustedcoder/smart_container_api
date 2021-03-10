from .. import db
from .users import User
import datetime


class Meals(db.Model):
    """
    Meals model for meals
    """
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    name = db.Column(db.String(225),nullable=False)
    cook_time = db.Column(db.String(225), nullable=False)
    image = db.Column(db.String(225), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now())

    def __init__(self,user_id,name,cook_time,image):
        self.user_id = user_id
        self.name = name
        self.cook_time = cook_time
        self.image = image
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return self.name
