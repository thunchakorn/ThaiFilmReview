from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, CreateView, ListView
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin

from reviews.models import Review, Like, Comment
from films.models import Film


class ReviewListView(ListView):
    model = Review
    paginate_by = 2
    context_object_name = "review_list"
    ordering = ["-created_at"]

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return ["reviews/partials/review_list.html"]
        return super().get_template_names()

    def get_queryset(self):
        query_profile_id = self.request.GET.get("profile_id")
        query_film_id = self.request.GET.get("film_id")

        qs = self.model.objects.with_like_and_comment(
            profile=(
                self.request.user.profile
                if self.request.user.is_authenticated
                else None
            )
        )

        if query_profile_id:
            qs = qs.filter(profile_id=query_profile_id)

        if query_film_id:
            qs = qs.filter(film_id=query_film_id)

        if not (query_profile_id or query_film_id):
            qs = qs.filter(profile_id__in=self.request.user.profile.followings.all())

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            qs = qs.order_by(*ordering)

        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["profile_id"] = self.request.GET.get("profile_id")
        return ctx


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

        review = Review.objects.with_like_and_comment(
            profile=self.request.user.profile
        ).get(id=pk)

        return render(
            request,
            self.template_name,
            context={"review": review},
        )


class CommentReview(LoginRequiredMixin, View):
    template_name = "reviews/partials/review_comment.html"

    def post(self, request, pk: int):
        comment = Comment.objects.create(
            profile=request.user.profile, review_id=pk, text=request.POST["text"]
        )
        comment.save()

        return render(
            request,
            self.template_name,
            context={"comment": comment},
        )


class ReviewDetailView(DetailView):
    model = Review

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.user.is_authenticated:
            return self.model.objects.with_like_and_comment(
                profile=self.request.user.profile
            )

        return self.model.objects.with_like_and_comment()


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
