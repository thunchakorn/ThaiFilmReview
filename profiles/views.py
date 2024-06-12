from typing import Any

from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views import View
from django.views.generic import DetailView, UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Exists, OuterRef
from django.contrib.messages.views import SuccessMessageMixin

from .models import Profile
from .forms import ProfileForm


class ProfileDetail(DetailView):
    model = Profile

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.annotate(
            followers_count=Count("followers", distinct=True),
            reviews_count=Count("reviews", distinct=True),
            likes_received_count=Count(
                "reviews__likes", filter=Q(reviews__likes__value=1)
            ),
        )

        if self.request.user.is_authenticated:
            qs = qs.annotate(
                is_follow=Exists(
                    Profile.objects.filter(
                        user=self.request.user, followings=OuterRef("pk")
                    )
                )
            )

        return qs


class ProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profiles/profile_form.html"
    success_message = "อัปเดตโปรไฟล์สำเร็จ"  # from SuccessMessageMixin

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        obj = self.model.objects.filter(pk=self.request.user.profile.id).get()
        return obj

    def form_valid(self, form):
        object = form.save(commit=False)

        if self.request.FILES:
            object.profile_pic = self.request.FILES["profile_pic"]

        object.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("profiles:detail", kwargs={"slug": self.object.slug})


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, slug):
        target_profile = get_object_or_404(Profile, slug=slug)
        user_profile = request.user.profile

        if user_profile == target_profile:
            return HttpResponseForbidden("Cannot follow yourself")

        if target_profile.followers.filter(id=user_profile.id).exists():
            target_profile.followers.remove(user_profile)
            return HttpResponse("Follow", content_type="text/plain")
        else:
            target_profile.followers.add(user_profile)
            return HttpResponse("Unfollow", content_type="text/plain")
