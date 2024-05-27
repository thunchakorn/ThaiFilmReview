import io
import pytest
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser_", password="testpass"
    )


def test_profile_str_method(user):
    profile = user.profile
    assert str(profile) == "testuser_"


def test_profile_slugify(user):
    profile = user.profile
    assert profile.slug == "testuser"


def test_profile_slugify(user):
    profile = user.profile
    assert profile.slug == "testuser"


@pytest.mark.parametrize(
    "dimesion, expected", [((100, 100), (100, 100)), ((500, 500), (200, 200))]
)
def test_image_resize(user, dimesion, expected):
    profile = user.profile

    img = Image.new("RGB", dimesion)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")

    image = SimpleUploadedFile(
        name="test_image.jpg", content=b"", content_type="image/jpeg"
    )
    image.file = buffer

    profile.profile_pic = image
    profile.save()

    assert profile.profile_pic._get_image_dimensions() == expected
