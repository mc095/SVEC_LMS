from django.contrib.auth.backends import ModelBackend
from .models import Lms_Users

class RollNumberBackend(ModelBackend):
    def authenticate(self, request, rollno=None, password=None, **kwargs):
        try:
            user = Lms_Users.objects.get(rollno=rollno)
            if user.check_password(password):
                return user
        except Lms_Users.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Lms_Users.objects.get(pk=user_id)
        except Lms_Users.DoesNotExist:
            return None
