from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


from films.models import Film, Person


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    screenplay_rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    acting_rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    production_rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cinematography_rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    sound_rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_spoiler = models.BooleanField(null=True, blank=True)
    short_review = models.CharField(max_length=64)
    full_review = models.CharField(max_length=12000)
    mvp_actor = models.ForeignKey(Person, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "film"], name="unique_review")
        ]

    def __str__(self) -> str:
        return f"{self.user}: {self.film}"


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)


class Like(models.Model):
    class LikeValue(models.IntegerChoices):
        LIKE = 1
        DISLIKE = 0

    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    value = models.IntegerField(choices=LikeValue)
