from django.contrib.auth.backends import ModelBackend
from allauth.account.auth_backends import AuthenticationBackend
from django.contrib.auth.models import User


class CustomAuthenticationBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            user = User.objects.select_related("profile").get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


class CustomAllAuthAuthenticationBackend(AuthenticationBackend):
    def get_user(self, user_id):
        try:
            user = User.objects.select_related("profile").get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
