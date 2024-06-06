from typing import Any
from django.db.models.query import QuerySet

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import (
    DetailView,
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
)
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django_htmx.http import HttpResponseClientRedirect

from reviews.models import Review, Like, Comment
from reviews.forms import ReviewForm

from films.models import Film


class ReviewListView(ListView):
    model = Review
    paginate_by = 5
    context_object_name = "review_list"
    ordering = ["-created_at"]

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return ["reviews/partials/review_list.html"]
        return super().get_template_names()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.with_like_and_comment(
            profile=(
                self.request.user.profile
                if self.request.user.is_authenticated
                else None
            )
        )

        query_profile_id = self.request.GET.get("profile_id")
        query_film_id = self.request.GET.get("film_id")

        if query_profile_id:
            qs = qs.filter(profile_id=query_profile_id)

        if query_film_id:
            qs = qs.filter(film_id=query_film_id)

        if self.request.user.is_authenticated and not (
            query_profile_id or query_film_id
        ):
            qs = qs.filter(profile_id__in=self.request.user.profile.followings.all())

        return qs.select_related("film", "profile")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["profile_id"] = self.request.GET.get("profile_id")
        return ctx


class LikeReview(View):
    template_name = "reviews/partials/review_likes_button.html"

    async def post(self, request, pk: int):
        user = await request.auser()

        if not user.is_authenticated and self.request.htmx:
            return HttpResponseClientRedirect(reverse("account_login"))

        profile = user.profile
        like_value = int(request.GET.get("value"))
        like_instance = await Like.objects.filter(
            profile=profile, review_id=pk
        ).afirst()

        if not like_instance:
            like = Like(review_id=pk, profile=profile, value=like_value)
            await like.asave()
        elif like_instance.value == like_value:
            await like_instance.adelete()
        else:
            like_instance.value = like_value
            await like_instance.asave()

        review = await Review.objects.with_like_and_comment(profile=profile).aget(id=pk)

        return render(
            request,
            self.template_name,
            context={"review": review},
        )


class CommentReview(LoginRequiredMixin, View):
    template_name = "reviews/partials/review_comment.html"

    def post(self, request, pk: int):
        comment = Comment.objects.create(
            profile=request.user.profile, review_id=pk, text=request.POST.get("text")
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
        qs = super().get_queryset()
        qs = qs.with_like_and_comment(
            profile=(
                self.request.user.profile
                if self.request.user.is_authenticated
                else None
            )
        )

        qs = qs.select_related("film", "profile")
        return qs


class ReviewCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ReviewForm
    template_name = "reviews/review_form.html"
    success_message = "สร้างรีวิว {film} สำเร็จ"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        film = get_object_or_404(Film, slug=self.kwargs["slug"])
        ctx["film"] = film
        return ctx

    def form_valid(self, form):
        film = get_object_or_404(Film, slug=self.kwargs["slug"])
        object = form.save(commit=False)

        object.profile = self.request.user.profile
        object.film = film

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("reviews:detail", kwargs={"pk": self.object.pk})

    def get_success_message(self, cleaned_data):
        return self.success_message.format(film=self.object.film)


class ReviewUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    template_name = "reviews/review_form.html"
    model = Review
    form_class = ReviewForm
    success_message = "แก้ไขรีวิว {film} สำเร็จ"

    def test_func(self):
        obj = self.get_object()
        return obj.profile == self.request.user.profile

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["film"] = ctx["object"].film
        return ctx

    def get_success_message(self, cleaned_data):
        return self.success_message.format(film=self.object.film)


class ReviewDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Review
    success_message = "ลบรีวิว {film} สำเร็จ"
    success_url = reverse_lazy("reviews:list")

    def test_func(self):
        obj = self.get_object()
        return obj.profile == self.request.user.profile

    def get_success_message(self, cleaned_data):
        return self.success_message.format(film=self.object.film)


class MarkSpoilerReviewView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ["reviews.mark_as_spoiler"]

    def post(self, request, pk: int):
        review = Review.objects.filter(pk=pk).first()
        review.is_spoiler = True
        review.save()
        text = _("Spoiler")
        return HttpResponse(f'<p class="text-error">{text}!</p>')
