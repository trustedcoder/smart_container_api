from .. import db
from .meals import Meals
from .containers import Containers
import datetime


class MealsIngredient(db.Model):
    """
    MealsIngredient model for ingredients
    """
    __tablename__ = 'meal_ingredient'

    meal_id = db.Column(db.Integer, db.ForeignKey(Meals.id), nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey(Containers.id), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now())
    __table_args__ = (db.PrimaryKeyConstraint('meal_id', 'container_id', name='_meal_id_uc'),)

    def __init__(self,meal_id,container_id):
        self.meal_id = meal_id
        self.container_id = container_id
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return self.name
