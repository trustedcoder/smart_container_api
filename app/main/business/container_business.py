from ..helper.auth_methods import AuthMethod
from ..model.containers import Containers
from ..model.readings import Readings
from ..model.users import User
from ..helper.user_method import UserMethod
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
                        .query.filter(Containers.public_id == data['container_id'], Containers.user_id is None).first()
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

                    response_object = {
                        'status': 1,
                        'name': label,
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
                    found_container.name_item = data['d']

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
            try:
                db.session.commit()

                if found_container.is_calibrated:
                    new_data = Readings(
                        container_id=found_container.id,
                        weight = data['weight'],
                        level = data['level']
                    )
                    UserMethod.save_changes(new_data)
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
                found_container = Containers.query.filter(Containers.public_id == data['container_id'],
                                                          Containers.user_id == resp['user_id']).first()
                if found_container:
                    found_container.is_calibrated = True
                    found_container.total_weight = found_container.current_weight
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
    def get_containers(auth_token):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                found_containers = Containers.query.filter(Containers.user_id == resp['user_id']).all()
                if found_containers:
                    list_container = []
                    for container in found_containers:
                        list_container.append({
                            'name_item': container.name_item,
                            'remaining': container.current_weight,
                            'name_container': container.name_container,
                            'image': '',
                            'percentage': '10%',
                            'public_id': container.public_id
                        })
                    response_object = {
                        'status': 1,
                        'data': list_container,
                        'message': 'container found'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 0,
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
                        list_data = {
                            'weight': read.weight,
                            'level': read.level,
                            'date_created': read.date_created
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

                    response_object = {
                        'status': 1,
                        'name_item': found_containers.name_item,
                        'remaining': found_containers.current_weight,
                        'capacity': found_containers.t,
                        'state': '',
                        'countable': '',
                        'quantity': '',
                        'name_container': found_containers.name_container,
                        'image': '',
                        'percentage': '10%',
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

