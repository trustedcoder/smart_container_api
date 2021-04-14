from ..helper.auth_methods import AuthMethod
from ..model.containers import Containers
from ..model.readings import Readings
from ..model.notification import Notification
from ..model.users import User
from ..model.meal_ingredients import MealsIngredient
from ..model.meals import Meals
from ..model.shopping import Shopping
from ..helper.user_method import UserMethod
from ..helper.shop_methods import ShopMethod
from ..helper.notify_methods import NotifyMethod
from ..helper.container_methods import ContainerMethod
from flask import current_app as app
from app.main import db
from definitions import ROOT_DIR
import os,datetime
import cv2
import cvlib as cv


class ContainerBusiness:
    @staticmethod
    def add_container_one(auth_token,data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                found_container = Containers.query.filter(Containers.public_id == data['container_id']).first()
                if found_container:
                    is_container_fresh = Containers\
                        .query.filter(Containers.public_id == data['container_id'], Containers.user_id == None).first()
                    if is_container_fresh:
                        if data['state'] == 'Liquid':
                            state = 1
                        elif data['state'] == 'Solid':
                            state = 2
                        else:
                            state = 0
                        is_container_fresh.name_container = data['name']
                        is_container_fresh.state = state
                        is_container_fresh.is_edible = data['is_edible']
                        is_container_fresh.user_id = resp['user_id']

                        try:
                            db.session.commit()
                            response_object = {
                                'status': 1,
                                'container_id': is_container_fresh.id,
                                'message': 'Details saved'
                            }
                            return response_object
                        except Exception as e:
                            db.session.rollback()
                            response_object = {
                                'status': 0,
                                'message': str(e)
                            }
                            return response_object
                    response_object = {
                        'status': 0,
                        'message': 'This container is already assigned.'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'Container not found.'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def detect_object(auth_token,data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                # generate a key name for the file
                name = ('\n'.join(map(str, AuthMethod.random_number(1, 2, 10000000000000000000000))))
                # get the real name of the uploaded file
                real_name = data['image'].filename
                # get the file extension
                extension = real_name.rsplit('.', 1)[1].lower()
                try:
                    destination = os.path.join('app/main/static/' + name + '/')
                    if not os.path.exists(destination):
                        os.makedirs(destination)
                    image_file = '%s%s' % (destination, real_name)
                    data['image'].save(image_file)

                    # save saved name of the file in the store database table

                    im = cv2.imread(ROOT_DIR + '/app/main/static/' + name + '/'+real_name)
                    bbox, label, conf = cv.detect_common_objects(im)

                    found_container = Containers.query.filter(Containers.public_id == data['container_id']).first()
                    found_container.image_item = name + '/' +real_name

                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                    if len(label) > 0:
                        name_b = label[0]
                    else:
                        name_b = ''
                    response_object = {
                        'status': 1,
                        'name': name_b,
                        'message': 'Object detected'
                    }
                    return response_object
                except Exception as e:
                    response_object = {
                        'status': 0,
                        'message': 'An error occurred' + str(e)
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def add_container_two(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                found_container = Containers.query.filter(Containers.public_id == data['container_id'],Containers.user_id == resp['user_id']).first()
                if found_container:
                    found_container.is_countable = data['is_countable']
                    found_container.name_item = data['name_item']

                    try:
                        db.session.commit()
                        response_object = {
                            'status': 1,
                            'is_countable': data['is_countable'],
                            'message': 'Details saved'
                        }
                        return response_object
                    except Exception as e:
                        db.session.rollback()
                        response_object = {
                            'status': 0,
                            'message': str(e)
                        }
                        return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'This container does not belong to you.'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def update_weight_level(data):
        found_container = Containers.query.filter(Containers.public_id == data['container_id']).first()
        if found_container:
            found_container.current_weight = data['weight']
            found_container.current_level = data['level']

            # update weight of one item (to be used to get total quantity of item)
            if found_container.is_countable:
                if found_container.one_item_weight is None:
                    found_container.one_item_weight = data['weight']
                if found_container.total_weight is not None:
                    # add or remove from shopping list
                    ShopMethod.add_to_shop(found_container.id)
            else:
                if found_container.total_level is not None:
                    # add or remove from shopping list
                    ShopMethod.add_to_shop(found_container.id)
            try:
                db.session.commit()
                if found_container.is_calibrated:
                    new_data = Readings(
                        container_id=found_container.id,
                        weight = str(data['weight']),
                        level = str(data['level'])
                    )
                    UserMethod.save_changes(new_data)

                    # send push notification and email alerts
                    is_send_notification = False
                    title = 'Smart container'
                    message = ''
                    image_id = 1
                    if ContainerMethod.is_empty(found_container.id):
                        is_send_notification = True
                        message = 'Your ' + str(found_container.name_item) + ' container is empty, please refill'
                        image_id = 1
                    if ContainerMethod.is_low(found_container.id):
                        is_send_notification = True
                        message = 'Your ' + str(found_container.name_item) + ' is about to exhaust, please refill'
                        image_id = 2
                    if ContainerMethod.is_half(found_container.id):
                        is_send_notification = True
                        message = 'Your ' + str(found_container.name_item) + ' container have gone below half, consider refilling'
                        image_id = 3
                    if is_send_notification:
                        found_notification = Notification.query \
                            .filter(Notification.user_id == found_container.user_id,
                                    Notification.container_id == found_container.id) \
                            .order_by(Notification.id.desc()).first()
                        if found_notification:
                            elapsed_time = datetime.datetime.now() - found_notification.date_created
                            if elapsed_time.total_seconds() > 3:
                                new_notify = Notification(
                                    container_id=found_container.id,
                                    user_id=found_container.user_id,
                                    title=message,
                                    image=image_id
                                )
                                AuthMethod.save_changes(new_notify)
                                found_user = User.query.filter(User.id == found_container.user_id).first()
                                if found_user:
                                    push_data = {
                                        'registration_ids': [found_user.fcm_token],
                                        'title': title,
                                        'message': message,
                                        'image_id': image_id
                                    }
                                    email_data = {
                                        'from': 'alert@smartcontainer.link',
                                        'to': found_user.email,
                                        'subject': title,
                                        'text': message,
                                        'html': '',
                                    }
                                    NotifyMethod.fcm_send_push(push_data)
                                    NotifyMethod.mailjet_send_email(email_data)
                        else:
                            new_notify = Notification(
                                container_id=found_container.id,
                                user_id=found_container.user_id,
                                title=message,
                                image=image_id
                            )
                            AuthMethod.save_changes(new_notify)
                            found_user = User.query.filter(User.id == found_container.user_id).first()
                            if found_user:
                                push_data = {
                                    'registration_ids': [found_user.fcm_token],
                                    'title': title,
                                    'message': message,
                                    'image_id': image_id
                                }
                                email_data = {
                                    'from': 'alert@smartcontainer.link',
                                    'to': found_user.email,
                                    'subject': title,
                                    'text': message,
                                    'html': '',
                                }
                                NotifyMethod.fcm_send_push(push_data)
                                NotifyMethod.mailjet_send_email(email_data)

                response_object = {
                    'status': 1,
                    'message': 'Details saved'
                }
                return response_object
            except Exception as e:
                db.session.rollback()
                response_object = {
                    'status': 0,
                    'message': str(e)
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'This container does not belong to you.'
            }
            return response_object

    @staticmethod
    def calibrate(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                found_container = Containers.query.filter(Containers.public_id == data['container_id'],Containers.user_id == resp['user_id']).first()
                if found_container:
                    found_container.is_calibrated = True
                    found_container.total_weight = found_container.current_weight
                    found_container.total_level = found_container.current_level
                    try:
                        db.session.commit()
                        response_object = {
                            'status': 1,
                            'message': 'Container calibrated'
                        }
                        return response_object
                    except Exception as e:
                        db.session.rollback()
                        response_object = {
                            'status': 0,
                            'message': str(e)
                        }
                        return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'This container does not belong to you.'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def get_containers(auth_token,data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                found_containers = Containers.query.filter(Containers.user_id == resp['user_id']).limit(app.config["PAGINATION_COUNT"]).offset(data["start"]).all()
                if found_containers:
                    list_container = []
                    for container in found_containers:
                        if container.is_countable:
                            unit = 'kg'
                        else:
                            unit = 'cm'

                        if ContainerMethod.get_item_percent_remaining(container.id) >30:
                            image_url = 'static/ic_container_green.png'
                        elif ContainerMethod.get_item_percent_remaining(container.id) >= 10:
                            image_url = 'static/ic_container_orange.png'
                        else:
                            image_url = 'static/ic_container_red.png'
                        list_container.append({
                            'name_item': container.name_item,
                            'remaining': str("{:.2f}".format(ContainerMethod.get_item_weight_level_remaining(container.id)))+unit,
                            'name_container': container.name_container,
                            'image': image_url,
                            'percentage': "{:.2f}".format(ContainerMethod.get_item_percent_remaining(container.id)),
                            'public_id': container.public_id
                        })

                    # pagination
                    total_rows = Containers.query.filter(Containers.user_id == resp['user_id']).count()

                    if total_rows <= ((data["start"] + app.config["PAGINATION_COUNT"])):
                        is_last_page = True
                    else:
                        is_last_page = False

                    response_object = {
                        'status': 1,
                        'data': list_container,
                        "is_last_page": is_last_page,
                        'message': 'container found'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 1,
                        'data': [],
                        'message': 'No container found'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def view_container(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                found_containers = Containers.query.filter(Containers.public_id == data['container_id']).first()
                if found_containers:
                    reading = Readings.query.filter(Readings.container_id == found_containers.id)

                    # filter by 7 days
                    current_time = datetime.datetime.utcnow()
                    _7_days_ago = current_time - datetime.timedelta(days=7)
                    reading = reading.filter(Readings.date_created > _7_days_ago)

                    # order date
                    reading = reading.order_by(Readings.date_created.desc())

                    readings = reading.all()

                    list_reading = []
                    for read in readings:
                        is_add = True
                        if found_containers.is_countable:
                            value = read.weight
                        else:
                            value = read.level
                        list_data = {
                            'value': float(value),
                            'date_created': str(read.date_created.strftime("%d %b"))
                        }
                        # check if its the last reading for that day
                        for check_read in readings:
                            check_date = check_read.date_created.date()
                            my_date = read.date_created.date()
                            if check_date == my_date:
                                if check_read.date_created > read.date_created:
                                    is_add = False

                        if is_add:
                            list_reading.append(list_data)
                    if found_containers.is_countable:
                        unit = 'kg'
                        yes = 'Yes'
                    else:
                        unit = 'cm'
                        yes = 'No'
                    if found_containers.state ==  app.config["STATE_SOLID"]:
                        state = 'Solid'
                    elif found_containers.state == app.config["STATE_LIQUID"]:
                        state = 'Liquid'
                    else:
                        state = 'Gas'
                    response_object = {
                        'status': 1,
                        'name_item': found_containers.name_item,
                        'remaining': str(ContainerMethod.get_item_weight_level_remaining(found_containers.id))+unit,
                        'capacity': str(ContainerMethod.get_container_capacity(found_containers.id))+unit,
                        'state': state,
                        'countable': yes,
                        'quantity': ContainerMethod.get_item_quantity(found_containers.id),
                        'name_container': found_containers.name_container,
                        'image': 'static/'+str(found_containers.image_item),
                        'percentage': str("{:.2f}".format(ContainerMethod.get_item_percent_remaining(found_containers.id))),
                        'data': list_reading,
                        'message': 'container found'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'No container found'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def check_for_one(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                found_containers = Containers.query.filter(Containers.public_id == data['container_id']).first()
                if found_containers:
                    if found_containers.is_countable:
                        if found_containers.one_item_weight is not None:
                            response_object = {
                                'status': 1,
                                'current_reading': str(ContainerMethod.get_item_weight_level_remaining(found_containers.id))+' kg',
                                'message': 'You can now add all the other items'
                            }
                            return response_object
                        else:
                            response_object = {
                                'status': 1,
                                'current_reading': str(ContainerMethod.get_item_weight_level_remaining(found_containers.id))+' kg',
                                'message': 'Please add one of the item.'
                            }
                            return response_object
                    else:
                        response_object = {
                            'status': 1,
                            'current_reading': str(ContainerMethod.get_item_weight_level_remaining(found_containers.id))+' cm',
                            'message': 'You can fill the container'
                        }
                        return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'No container found'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def delete_container(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                found_container = Containers.query.filter(Containers.public_id == data['container_id'], Containers.user_id == resp['user_id']).first()
                if found_container:
                    #update the container
                    found_container.user_id = None
                    found_container.state = None
                    found_container.is_edible = None
                    found_container.total_weight = None
                    found_container.one_item_weight = None
                    found_container.total_level = None
                    found_container.current_weight = None
                    found_container.current_level = None
                    found_container.image_container = None
                    found_container.image_item = None
                    found_container.name_container = None
                    found_container.name_item = None
                    found_container.is_countable = None
                    found_container.is_calibrated = None
                    found_container.status = 0

                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()

                    #  delete all meal ingredient
                    MealsIngredient.query.filter(MealsIngredient.container_id == found_container.id).delete()
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()

                    #  delete all notification
                    Notification.query.filter(Notification.container_id == found_container.id).delete()
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()

                    #  delete all readings
                    Readings.query.filter(Readings.container_id == found_container.id).delete()
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()

                    #  delete all readings
                    Shopping.query.filter(Shopping.container_id == found_container.id).delete()
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()

                    response_object = {
                        'status': 1,
                        'message': 'Container deleted'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'Container not found.'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object