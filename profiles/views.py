from typing import Any

from django.db.models.query import QuerySet
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Exists, OuterRef
from django.contrib import messages

from profiles.models import Profile
from profiles.forms import ProfileForm


class ProfileDetail(DetailView):
    model = Profile

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.annotate(
            followers_count=Count("followers", distinct=True),
            reviews_count=Count("reviews", distinct=True),
            likes_received_count=Count("reviews", filter=Q(reviews__likes__value=1)),
        )

        if self.request.user.is_authenticated:
            qs = qs.annotate(
                is_profile_follow=Exists(
                    Profile.objects.filter(
                        id=OuterRef(
                            "id",
                        ),
                        followers=self.request.user.profile,
                    )
                )
            )

        return qs


class ProfileUpdate(LoginRequiredMixin, View):
    template_name = "profiles/profile_form.html"

    def get(self, request):
        profile = get_object_or_404(Profile, id=request.user.profile.id)
        form = ProfileForm(instance=profile)
        ctx = {"form": form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        profile = get_object_or_404(Profile, id=request.user.profile.id)
        if request.FILES:
            request.FILES["profile_pic"].name = f"{request.user.username}.jpg"
        form = ProfileForm(request.POST, request.FILES or None, instance=profile)

        if not form.is_valid():
            ctx = {"form": form}
            return render(request, self.template_name, ctx)

        profile = form.save()
        messages.add_message(request, messages.SUCCESS, "อัปเดตโปรไฟล์สำเร็จ")

        return redirect(reverse("profiles:detail", kwargs={"slug": profile.slug}))


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, slug):
        target_profile = get_object_or_404(Profile, slug=slug)
        user_profile = request.user.profile

        if user_profile == target_profile:
            return HttpResponseNotAllowed("Cannot follow yourself")

        if target_profile.followers.filter(id=user_profile.id).exists():
            target_profile.followers.remove(user_profile)
            return HttpResponse("Follow")
        else:
            target_profile.followers.add(user_profile)
            return HttpResponse("Unfollow")
