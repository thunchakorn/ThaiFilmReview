from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from allauth.account.auth_backends import AuthenticationBackend


class CustomAuthenticationBackend(ModelBackend):
    # since User's profile is always need, optimize by select_related
    def get_user(self, user_id):
        try:
            User = get_user_model()
            user = User.objects.select_related("profile").get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


class CustomAllAuthAuthenticationBackend(AuthenticationBackend):
    # since User's profile is always need, optimize by select_related
    def get_user(self, user_id):
        try:
            User = get_user_model()
            user = User.objects.select_related("profile").get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
