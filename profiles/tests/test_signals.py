from profiles.models import Profile


def test_create_profile_from_signal(django_user_model):

    assert Profile.objects.count() == 0

    new_user = django_user_model.objects.create(username="abc", password="def")

    assert Profile.objects.first().user == new_user
