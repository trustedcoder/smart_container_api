from .. import db
from .containers import Containers
from .users import User
import datetime


class Notification(db.Model):
    """
    Notification model for notification
    """
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    container_id = db.Column(db.Integer, db.ForeignKey(Containers.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(225),nullable=False)
    image = db.Column(db.String(225), nullable=False)
    is_opened = db.Column(db.Boolean, nullable=False, default=False)
    date_created = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now())

    def __init__(self,container_id,user_id,title,image):
        self.container_id = container_id
        self.user_id = user_id
        self.title = title
        self.image = image
        self.is_opened = False
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return self.container_id
