from .. import db
from .containers import Containers
import datetime


class Readings(db.Model):
    """
    Readings model for readings
    """
    __tablename__ = 'readings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    container_id = db.Column(db.Integer, db.ForeignKey(Containers.id), nullable=False)
    weight = db.Column(db.String(225),nullable=False)
    level = db.Column(db.String(225), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now())

    def __init__(self,container_id,weight,level):
        self.container_id = container_id
        self.weight = weight
        self.level = level
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return self.container_id
