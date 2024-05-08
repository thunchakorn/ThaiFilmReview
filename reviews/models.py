from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


from films.models import Film, Person
from profiles.models import Profile


class Review(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="reviews"
    )
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="reviews")
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
    mvp_actor = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="mvps",
        # limit_choices_to=Q(acted_films__id=F("film")),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["profile", "film"], name="unique_review")
        ]

    def __str__(self) -> str:
        return f"{self.profile}-{self.film}"


class Comment(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f"{self.review}:{self.id}"


class Like(models.Model):
    class LikeValue(models.IntegerChoices):
        LIKE = 1
        DISLIKE = 0

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="likes")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="likes")
    value = models.IntegerField(choices=LikeValue)

    def __str__(self) -> str:
        return f"{self.review}:{self.get_value_display()}"
