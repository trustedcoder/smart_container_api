from ..model.notification import Notification


class NotifyMethod:
    @staticmethod
    def get_notify_total(user_id):
        total_notify = Notification.query.filter(Notification.user_id == user_id).count()
        return total_notify

