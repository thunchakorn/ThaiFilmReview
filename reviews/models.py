import uuid

from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

from films.models import Film
from profiles.models import Profile


class ReviewsManager(models.Manager):
    def with_like_and_comment(self, profile=None):
        self = self.annotate(
            likes__count=models.Count(
                "likes", filter=models.Q(likes__value=1), distinct=True
            ),
            dislikes__count=models.Count(
                "likes", filter=models.Q(likes__value=-1), distinct=True
            ),
            comments__count=models.Count("comments", distinct=True),
        )

        if profile:
            self = self.annotate(
                profile_like_value=models.Subquery(
                    Like.objects.filter(
                        profile=profile, review=models.OuterRef("pk")
                    ).values("value")
                )
            )

        return self


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="reviews"
    )
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="reviews")
    direction_rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    screenplay_rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    acting_rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    visual_rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    sound_rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    overall_rating = models.FloatField(
        null=False, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    is_spoiler = models.BooleanField(null=True, blank=True)
    short_review = models.CharField(max_length=64)
    full_review = models.CharField(max_length=12000)

    created_at = models.DateTimeField(auto_now_add=True)
    objects = ReviewsManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["profile", "film"], name="unique_review")
        ]

    def __str__(self) -> str:
        return f"{self.profile}-{self.film}"

    def get_absolute_url(self):
        # define this to be able to view on site on admin page
        # and object.get_absolute_url in template
        return reverse("reviews:detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    class Meta:
        ordering = [
            "-created_at",
        ]

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.CharField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.review}:{self.id}"


class Like(models.Model):
    class LikeValue(models.IntegerChoices):
        LIKE = 1
        DISLIKE = -1

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="likes")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="likes")
    value = models.IntegerField(choices=LikeValue)

    def __str__(self) -> str:
        return f"{self.profile}->{self.review}:{self.get_value_display()}"
