from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin

from reviews.models import Review, Like, Comment
from reviews.forms import ReviewForm

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

        if self.request.user.is_authenticated and not (
            query_profile_id or query_film_id
        ):
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


class LikeReview(View):
    template_name = "reviews/partials/review_likes_button.html"

    def post(self, request, pk: int):

        if not request.user.is_authenticated and self.request.htmx:
            response = HttpResponse("Login")
            response["HX-Redirect"] = reverse("account_login")
            return response

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


class ReviewCreateView(LoginRequiredMixin, View):
    form_class = ReviewForm
    template_name = "reviews/review_form.html"

    def get(self, request, **kwargs):
        form = ReviewForm()
        film = get_object_or_404(Film, slug=kwargs["slug"])
        ctx = {"form": form, "film": film}
        return render(request, self.template_name, ctx)

    def post(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        form = ReviewForm(request.POST)
        film = get_object_or_404(Film, slug=kwargs["slug"])
        if not form.is_valid():
            ctx = {"form": form}
            return render(request, self.template_name, ctx)

        form.instance.profile = self.request.user.profile
        form.instance.film = film

        review = form.save()

        return redirect(reverse("reviews:detail", kwargs={"pk": review.pk}))
