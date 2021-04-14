from app.main import db
from app.main.model.meal_ingredients import MealsIngredient


class MealMethod:
    @staticmethod
    def is_found_ingredient(meal_id, container_id):
        found = MealsIngredient.query.filter(MealsIngredient.meal_id==meal_id, MealsIngredient.container_id == container_id).first()
        if found:
            return True
        else:
            return False

    @staticmethod
    def get_ingredient_q(meal_id, container_id):
        found = MealsIngredient.query.filter(MealsIngredient.meal_id == meal_id,MealsIngredient.container_id == container_id).first()
        if found:
            return found.quantity_one
        else:
            return '0'