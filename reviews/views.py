from typing import Any
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, CreateView, ListView
from django.urls import reverse
from django.db.models import Count, Q, Subquery, OuterRef

from django.contrib.auth.mixins import LoginRequiredMixin

from reviews.models import Review, Like
from films.models import Film


class ReviewListView(ListView):
    model = Review
    paginate_by = 2
    context_object_name = "review_list"
    ordering = ["-created_at"]

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return ["reviews/partials/review_list_element.html"]
        return super().get_template_names()

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.is_authenticated:
            qs = qs.filter(profile_id__in=self.request.user.profile.followings.all())
            qs = qs.annotate(
                is_like_by_profile=Subquery(
                    Like.objects.filter(
                        profile=self.request.user.profile, review=OuterRef("pk")
                    ).values("value")
                )
            )

        qs = qs.annotate(
            likes__count=Count("likes", filter=Q(likes__value=1)),
            dislikes__count=Count("likes", filter=Q(likes__value=-1)),
            comments__count=Count("comments"),
        )

        return qs


class LikeReview(LoginRequiredMixin, View):
    template_name = "reviews/partials/review_likes_button.html"

    def post(self, request, pk: int):
        profile = self.request.user.profile
        like_value = int(request.GET["value"])
        like_instance = Like.objects.filter(profile=profile, review_id=pk).first()

        if not like_instance:
            like = Like(review_id=pk, profile=profile, value=like_value)
            like.save()
        elif like_instance.value == like_value:
            like_instance.delete()
        else:
            like_instance.value = like_value
            like_instance.save()

        qs = Review.objects.filter(id=pk).annotate(
            likes__count=Count("likes", filter=Q(likes__value=1)),
            dislikes__count=Count("likes", filter=Q(likes__value=-1)),
            comments__count=Count("comments"),
            is_like_by_profile=Subquery(
                Like.objects.filter(
                    profile=self.request.user.profile, review=OuterRef("pk")
                ).values("value")
            ),
        )

        return render(
            request,
            self.template_name,
            context={"review": qs.first()},
        )


class ReviewDetailView(DetailView):
    model = Review


class ReviewCreateView(CreateView, LoginRequiredMixin):
    model = Review
    fields = [
        "film",
        "rating",
        "screenplay_rating",
        "acting_rating",
        "production_rating",
        "cinematography_rating",
        "sound_rating",
        "is_spoiler",
        "short_review",
        "full_review",
        "mvp_actor",
    ]

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self) -> str:
        id = self.object.id
        return reverse("reviews:detail", kwargs={"pk": id})

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        if "film_id" in self.request.GET:
            film_id = self.request.GET["film_id"]
            initial["film"] = Film.objects.get(id=film_id)
        return initial
