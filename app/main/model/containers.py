from .. import db
from .users import User
import datetime


class Containers(db.Model):
    """
    Containers Model for containers
    """
    __tablename__ = 'containers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(255),unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    state = db.Column(db.Integer, nullable=True)
    is_edible = db.Column(db.Boolean, nullable=True)
    total_weight = db.Column(db.String(255), nullable=True)
    one_item_weight = db.Column(db.String(255), nullable=True)
    total_level = db.Column(db.String(255), nullable=True)
    current_weight = db.Column(db.String(255), nullable=True, default = '0')
    current_level = db.Column(db.String(255), nullable=True, default = '0')
    image_container = db.Column(db.String(255), nullable=True)
    image_item = db.Column(db.String(255), nullable=True)
    name_container = db.Column(db.String(255), nullable=True)
    name_item = db.Column(db.String(255), nullable=True)
    is_countable = db.Column(db.Boolean, nullable=True)
    is_calibrated = db.Column(db.Boolean, nullable=True)
    status = db.Column(db.Integer,nullable=True)
    date_created = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now())

    def __init__(self,public_id,status):
        self.public_id = public_id
        self.status = status
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return self.public_id
