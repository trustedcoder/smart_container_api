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
            api_key="AAAAV73IL1k:APA91bEdZQQAdJQEtIQ-6p-ZALuOyQEuONrGX7pulyosc-m2oOXJq5T4UYJ7-Y5A4tS06n4uHKSHsViYoRVV7E3hi4zgGe9IST6Dyrrz3wtb9evP-DZYCH_gLMyoHLpMsqg5DnGazvPk"
        )
        # registration_ids is list of fcm_tokens
        registration_ids = data["registration_ids"]

        data_message = {
            "title": data['title'],
            "message": data['message'],
            "image_id": data['image_id']
        }
        push_service.notify_multiple_devices(
            registration_ids=registration_ids,
            data_message = data_message
        )
        print(registration_ids)

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

