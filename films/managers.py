from django.db import models


class FilmManager(models.QuerySet):
    def with_reviews_data(self, profile=None):
        self = self.annotate(
            reviews_count=models.Count("reviews"),
            average_rating=models.Avg("reviews__overall_rating"),
        )

        if profile:
            self = self.annotate(
                is_user_review=models.Exists(
                    self.filter(id=models.OuterRef("id"), reviews__profile=profile)
                )
            )

        return self
