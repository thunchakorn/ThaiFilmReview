from django.test import TestCase
from django.contrib.auth import get_user_model

from profiles.models import Profile


class ProfileModelTests(TestCase):
    def test_create_profile_from_signal(self):
        user_model = get_user_model()
        self.assertEqual(Profile.objects.count(), 0)

        new_user = user_model.objects.create(username="abc", password="def")

        self.assertEqual(Profile.objects.first().user, new_user)
