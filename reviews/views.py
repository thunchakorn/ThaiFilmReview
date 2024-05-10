from typing import Any
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, CreateView
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin

from reviews.models import Review
from films.models import Film


class ReviewListView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            reviews = Review.objects.all()
            cntx = {"review_list": reviews}
            return render(request, "reviews/review_list.html", cntx)
        else:
            reviews = Review.objects.all()
            cntx = {"review_list": reviews}
            return render(request, "reviews/review_list.html", cntx)


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
