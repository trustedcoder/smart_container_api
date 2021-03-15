from .. import db
from .containers import Containers
from .users import User
import datetime


class Shopping(db.Model):
    """
    Shopping model for shopping
    """
    __tablename__ = 'shopping'

    container_id = db.Column(db.Integer, db.ForeignKey(Containers.id), nullable=False)
    is_bought = db.Column(db.Boolean,nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now())
    __table_args__ = (db.PrimaryKeyConstraint('container_id', name='_user_id_uc'),)

    def __init__(self,container_id,is_bought):
        self.container_id = container_id
        self.is_bought = is_bought
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return self.container_id
