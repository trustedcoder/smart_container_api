from ..helper.container_methods import ContainerMethod
from ..model.shopping import Shopping
from app.main import db
from flask import current_app as app


class ShopMethod:
    @staticmethod
    def add_to_shop(container_id):
        is_empty = ContainerMethod.is_empty(container_id)
        is_low = ContainerMethod.is_low(container_id)
        found_shop = Shopping.query.filter(Shopping.container_id == container_id).first()
        if is_empty or is_low:
            if not found_shop:
                new_data = Shopping(
                    container_id = container_id,
                    is_bought=False
                )
                try:
                    db.session.add(new_data)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    raise
        else:
            if found_shop:
                try:
                    Shopping.query.filter(Shopping.container_id == container_id).delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    raise



