from ..model.containers import Containers
from flask import current_app as app


class ContainerMethod:
    @staticmethod
    def is_low(container_id):
        found_container = Containers.query.filter(Containers.id == container_id).first()
        if found_container:
            if found_container.is_countable:
                percent_remaining = (found_container.current_weight/found_container.total_weight)*100
                if (percent_remaining <= app.config["CONTAINER_LOW_PERCENT"]) and (percent_remaining >2):
                    return True
                else:
                    return False
            else:
                percent_remaining = (found_container.current_level/found_container.total_level)*100
                if (percent_remaining <= app.config["CONTAINER_LOW_PERCENT"]) and (percent_remaining >2):
                    return True
                else:
                    return False
        else:
            return True

    @staticmethod
    def is_empty(container_id):
        found_container = Containers.query.filter(Containers.id == container_id).first()
        if found_container:
            if found_container.is_countable:
                percent_remaining = (found_container.current_weight / found_container.total_weight) * 100
                if (percent_remaining <= app.config["CONTAINER_EMPTY_PERCENT"]) or (percent_remaining <= 2):
                    return True
                else:
                    return False
            else:
                percent_remaining = (found_container.current_level / found_container.total_level) * 100
                if (percent_remaining <= app.config["CONTAINER_EMPTY_PERCENT"]) or (percent_remaining <= 2):
                    return True
                else:
                    return False
        else:
            return True

    @staticmethod
    def is_half(container_id):
        found_container = Containers.query.filter(Containers.id == container_id).first()
        if found_container:
            if found_container.is_countable:
                percent_remaining = (found_container.current_weight / found_container.total_weight) * 100
                if (percent_remaining <= app.config["CONTAINER_HALF_PERCENT"]) and (percent_remaining <= 30):
                    return True
                else:
                    return False
            else:
                percent_remaining = (found_container.current_level / found_container.total_level) * 100
                if (percent_remaining <= app.config["CONTAINER_HALF_PERCENT"]) and (percent_remaining <= 30):
                    return True
                else:
                    return False
        else:
            return True

    @staticmethod
    def get_container_item_name(container_id):
        found_item = Containers.query.filter(Containers.id == container_id).first()
        if found_item:
            return found_item.name_item
        else:
            return ''

    @staticmethod
    def get_container_item_image(container_id):
        found_item = Containers.query.filter(Containers.id == container_id).first()
        if found_item:
            return found_item.image_item
        else:
            return ''

    @staticmethod
    def get_item_weight_level_remaining(container_id):
        found_item = Containers.query.filter(Containers.id == container_id).first()
        if found_item:
            if found_item.is_countable:
                return found_item.current_weight+' kg'
            else:
                return found_item.current_level + ' cm'
        else:
            return '0'

    @staticmethod
    def get_item_percent_remaining(container_id):
        found_item = Containers.query.filter(Containers.id == container_id).first()
        if found_item:
            if found_item.is_countable:
                percent = (found_item.current_weight/found_item.total_weight)*100
                return percent+' %'
            else:
                percent = (found_item.current_level / found_item.total_level) * 100
                return percent+' %'
        else:
            return '0'

    @staticmethod
    def get_item_quantity(container_id):
        found_item = Containers.query.filter(Containers.id == container_id).first()
        if found_item:
            if found_item.is_countable:
                quantity = (found_item.total_weight /found_item.current_weight)
                return int(round(quantity))
            else:
                return 0
        else:
            return 0

    @staticmethod
    def get_container_capacity(container_id):
        found_item = Containers.query.filter(Containers.id == container_id).first()
        if found_item:
            if found_item.is_countable:
                return found_item.total_weight+' kg'
            else:
                return found_item.total_level+' cm'
        else:
            return '0'
