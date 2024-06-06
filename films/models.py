import re

from django.urls import reverse
from django.db import models
from django.core.validators import RegexValidator
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import SuspiciousFileOperation

from common.utils import slugify


class OverwriteImageStorage(FileSystemStorage):
    def get_valid_name(self, name: str) -> str:
        s = str(name).strip().replace(" ", "_")
        s = re.sub(r"(?u)[^\u0E00-\u0E7Fa-zA-Z0-9-_.]", "", s)
        if s in {"", ".", ".."}:
            raise SuspiciousFileOperation("Could not derive file name from '%s'" % name)
        return s


class FilmManager(models.QuerySet):
    def with_reviews_data(self, profile=None):
        self = self.annotate(
            reviews_count=models.Count("reviews"),
            average_rating=models.Avg("reviews__overall_rating"),
        )

        if profile:
            self = self.annotate(
                is_user_review=models.Exists(
                    Film.objects.filter(
                        id=models.OuterRef("id"), reviews__profile=profile
                    )
                )
            )

        return self


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Film(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)
    poster = models.ImageField(
        null=True, blank=True, upload_to="film_poster/", storage=OverwriteImageStorage()
    )
    genres = models.ManyToManyField(to=Genre)
    actors = models.ManyToManyField(
        to=Person, through="Role", related_name="acted_films"
    )
    directors = models.ManyToManyField(to=Person, related_name="directed_films")
    slug = models.CharField(
        null=False,
        blank=True,
        max_length=200,
        validators=[RegexValidator(regex=r"^[\u0E00-\u0E7Fa-zA-Z0-9_]+\Z")],
        db_index=True,
    )
    objects = FilmManager.as_manager()

    def __str__(self) -> str:
        return f"{self.name} ({self.release_date.year})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("films:detail", kwargs={"slug": self.slug})


class Role(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="roles")
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.person}-{self.name}"


class Link(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="links")

    def __str__(self) -> str:
        return f"{self.film}-{self.name}"
