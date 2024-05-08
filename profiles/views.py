from typing import Any

from django.views.generic import DetailView

from profiles.models import Profile
from reviews.models import Like


class ProfileDetail(DetailView):
    model = Profile

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        likes_received_count = Like.objects.filter(
            review__profile=self.kwargs["pk"]
        ).count()

        context["likes_received_count"] = likes_received_count
        return context
