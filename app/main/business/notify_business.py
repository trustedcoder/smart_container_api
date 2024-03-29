import timeago
import datetime
from flask import current_app as app
from app.main.model.containers import Containers
from ..model.notification import Notification
from app.main.model.users import User
from app.main import db


class NotifyBusiness:
    @staticmethod
    def get_notifications(auth_token,data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                notification = Notification.query.filter(Notification.user_id == resp['user_id']).order_by(Notification.date_created.desc())
                notifications = notification.limit(app.config["PAGINATION_COUNT"]).offset(data["start"]).all()
                now = datetime.datetime.now()
                if notifications:
                    list_notification = []
                    for notification in notifications:
                        found_container = Containers.query.filter(Containers.id == notification.container_id).first()
                        list_notification.append({
                            'container_id': found_container.public_id,
                            'image': int(notification.image),
                            'title': notification.title,
                            'date_ago': timeago.format(notification.date_created, now)
                        })
                        notification_opened = Notification.query.filter(Notification.user_id == resp['user_id'], Notification.id == notification.id).first()
                        notification_opened.is_opened = True
                        try:
                            db.session.commit()
                        except Exception as e:
                            print(e)
                            pass
                    # pagination
                    total_rows = Notification.query.filter(Notification.user_id == resp['user_id']).count()

                    if total_rows <= ((data["start"] + app.config["PAGINATION_COUNT"])):
                        is_last_page = True
                    else:
                        is_last_page = False
                    response_object = {
                        'status': 1,
                        'data': list_notification,
                        "is_last_page": is_last_page,
                        'message': 'notifications found'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 1,
                        'data': [],
                        "is_last_page": True,
                        'message': 'No notification found'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    "is_last_page": True,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object
