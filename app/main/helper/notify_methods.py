from ..model.notification import Notification
from pyfcm import FCMNotification
from mailjet_rest import Client
import os


class NotifyMethod:
    @staticmethod
    def get_notify_total(user_id):
        total_notify = Notification.query.filter(Notification.user_id == user_id).count()
        return total_notify

    @staticmethod
    def fcm_send_push(data):
        push_service = FCMNotification(
            api_key="AAAAXRmWaZ0:APA91bEnfYwgeTOPULlFG0YwmDE9JIK-yZZuIZR6d-mviCtoXu_LrOReub0bh8QfU3MZ0oaI9gF7TPrcXbPg-t5fOz59G7OO2nezhJN1FRFrDpHunRbWG-SvmQcP7fvziHQx0L52gW9v"
        )
        # registration_ids is list of fcm_tokens
        registration_ids = data["registration_ids"]
        # message_title = data['title']
        # message_body = data['message']
        # data_message = {
        #     "title": data['title'],
        #     "message": data['message'],
        #     "notify_id": data['notify_id']
        # }
        push_service.notify_multiple_devices(
            registration_ids=registration_ids,
            message_title=data["title"],
            message_body=data["message"],
            click_action="http://127.0.0.1:7002/",
        )

    @staticmethod
    def mailjet_send_email(data):
        # From should contain dict with key Email and Name
        api_key = os.environ["MJ_APIKEY_PUBLIC"]
        api_secret = os.environ["MJ_APIKEY_PRIVATE"]
        mailjet = Client(auth=(api_key, api_secret), version="v3.1")
        data = {
            "Messages": [
                {
                    "From": data["from"],
                    "To": data["to"],
                    "TemplateLanguage": True,
                    "Subject": data["subject"],
                    "TextPart": data["text"],
                    "HTMLPart": data["html"],
                }
            ]
        }
        try:
            result = mailjet.send.create(data=data)
            print(result)
        except Exception as e:
            print(f" Error sending mail to {data['to']}")

