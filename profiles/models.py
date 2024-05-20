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
    slug = models.SlugField(default="", null=False, blank=True, max_length=200)

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
    # Open the image using Pillow
    img = Image.open(image)
    # check if either the width or height is greater than the max
    if img.width > width or img.height > height:
        output_size = (width, height)
        # Create a new resized “thumbnail” version of the image with Pillow
        img.thumbnail(output_size)
        # Find the file name of the image
        img_filename = Path(image.file.name).name
        # Spilt the filename on “.” to get the file extension only
        img_suffix = Path(image.file.name).name.split(".")[-1]
        # Use the file extension to determine the file type from the image_types dictionary
        img_format = image_types[img_suffix]
        # Save the resized image into the buffer, noting the correct file type
        buffer = io.BytesIO()
        img.save(buffer, format=img_format)
        # Wrap the buffer in File object
        file_object = File(buffer)
        # Save the new resized file as usual, which will save to S3 using django-storages
        image.save(img_filename, file_object)
