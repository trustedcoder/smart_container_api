from mailjet_rest import Client
import os


class EmailMethod:
    @staticmethod
    def send_reset_password(name,email_address,pin):
        body = "Hello "+str(name)+",<br><br>" \
               "We got a request to reset your Smart Container password.<br>" \
               "Enter the PIN below in the field provided:<br><br>"\
               "<b>" + str(pin)+"</b><br><br>" \
               "The PIN will expire within 24 hours.<br><br>"
        data = {
            'from': {
                "Email": "no-reply@smartx.tech",
                "Name": "Smart Container"
            },
            'to': [
                {
                    "Email": email_address,
                    "Name": name
                }
            ],
            'subject': "Smart Container: Password reset",
            'text': "",
            'html': body

        }
        EmailMethod.mailjet_send_email(data)

    @staticmethod
    def mailjet_send_email(data):
        # From should contain dict with key Email and Name
        api_key = os.getenv('MJ_APIKEY_PUBLIC')
        api_secret = os.getenv('MJ_APIKEY_PRIVATE')
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": data['from'],
                    "To": data['to'],
                    "Subject": data['subject'],
                    "TextPart": data['text'],
                    "HTMLPart": data['html']
                }
            ]
        }
        result = mailjet.send.create(data=data)
        print (result.status_code)
        print(result.json())