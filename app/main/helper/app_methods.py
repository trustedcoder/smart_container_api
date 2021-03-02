from app.main import db
from pyfcm import FCMNotification


class AppMethod:
    @staticmethod
    def fcm_send_panic_multiple(data):
        push_service = FCMNotification(
            api_key="AAAA8ZoIM1I:APA91bGrq6jaekl-LxzK783wMbVHn8ryI6ArU136oY4XF35A8ufW6jxm1wxG3AB2jz9croQ82kDPulhIbCEM8OMFue4ufzkqb2Vi-IanhFcmLTf3Pu59I7FOr270QVrxSpv_x3nouwo_")
        registration_ids = data['registration_ids']
        # message_title = data['title']
        # message_body = data['message']
        data_message = {
            "title": data['title'],
            "message": data['message'],
            "notify_id": data['notify_id'],
            "notify_type": data['notify_type']
        }
        push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)

    @staticmethod
    def save_changes(data):
        try:
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise