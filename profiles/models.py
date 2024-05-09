from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profile_pic/")
    bio = models.CharField(max_length=1000, null=True, blank=True)
    followings = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        null=True,
        blank=True,
    )
    slug = models.SlugField(default="", null=False, blank=True, max_length=200)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)
