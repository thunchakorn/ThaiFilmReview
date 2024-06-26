import pytest
from pytest_django import asserts
from django.urls import reverse
from allauth.socialaccount.models import SocialApp


@pytest.fixture
def site():
    social_app = SocialApp.objects.create(
        provider="google",
        name="google",
        client_id="1234567890",
        secret="0987654321",
    )
    return social_app


@pytest.fixture
def profiles(django_user_model):
    profile_1 = django_user_model.objects.create_user(
        username="user1", password="testpass"
    ).profile
    profile_2 = django_user_model.objects.create_user(
        username="user2", password="testpass"
    ).profile
    profile_3 = django_user_model.objects.create_user(
        username="user3", password="testpass"
    ).profile

    profile_1.followings.add(profile_2, profile_3)
    profile_2.followings.add(profile_1)
    profile_3.followings.add(profile_2)

    return [profile_1, profile_2, profile_3]


def test_profile_detail_followers_count(client, profiles):
    response = client.get(reverse("profiles:detail", kwargs={"slug": "user2"}))
    context = response.context
    user1 = context["object"]

    assert user1.followers_count == 2


def test_profile_detail_is_follow(client, profiles):
    response = client.get(reverse("profiles:detail", kwargs={"slug": "user1"}))
    context = response.context
    assert hasattr(context.get("object"), "is_follow") is False

    profile_2 = profiles[1]
    client.force_login(profile_2.user)
    response = client.get(reverse("profiles:detail", kwargs={"slug": "user1"}))
    context = response.context
    assert context.get("object").is_follow is True

    profile_3 = profiles[2]
    client.force_login(profile_3.user)
    response = client.get(reverse("profiles:detail", kwargs={"slug": "user1"}))
    context = response.context
    assert context.get("object").is_follow is False


def test_follow_toggle(client, profiles, site):
    response = client.post(
        reverse("profiles:follow", kwargs={"slug": "user1"}), follow=True
    )
    expected_url = f'{reverse("account_login")}?next={reverse("profiles:follow", kwargs={"slug": "user1"})}'
    asserts.assertRedirects(
        response,
        expected_url,
    )

    profile_1 = profiles[0]
    client.force_login(profile_1.user)
    response = client.post(reverse("profiles:follow", kwargs={"slug": "user1"}))
    assert response.status_code == 403

    response = client.post(reverse("profiles:follow", kwargs={"slug": "user2"}))
    assert response.status_code == 200
    assert response.content == b"Follow"

    response = client.post(reverse("profiles:follow", kwargs={"slug": "user2"}))
    assert response.status_code == 200
    assert response.content == b"Unfollow"
