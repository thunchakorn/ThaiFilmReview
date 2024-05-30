import os
import io
from pathlib import Path

from django.core.files import File
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage

from PIL import Image


class OverwriteStorage(FileSystemStorage):
    """
    Overwrite file if filename exists.
    """

    def get_available_name(self, name, **kwargs):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="profile_pic/", storage=OverwriteStorage()
    )
    bio = models.CharField(max_length=1000, null=True, blank=True)
    followings = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
    )
    slug = models.SlugField(null=False, blank=True, max_length=200)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username

    def save(self, commit=True, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)

        if self.profile_pic and commit:
            image_resize(self.profile_pic, 200, 200)

        return super().save(*args, **kwargs)


image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def image_resize(image, width, height):

    img = Image.open(image)

    if img.width > width or img.height > height:
        output_size = (width, height)
        img.thumbnail(output_size)
        img_filename = Path(image.file.name).name
        img_suffix = Path(image.file.name).name.split(".")[-1]
        img_format = image_types[img_suffix]
        buffer = io.BytesIO()
        img.save(buffer, format=img_format)
        file_object = File(buffer)
        image.save(img_filename, file_object)
