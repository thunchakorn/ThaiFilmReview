from typing import Any

from django.views import View
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.mixins import LoginRequiredMixin

from profiles.models import Profile
from profiles.forms import ProfileForm
from reviews.models import Like


class ProfileDetail(DetailView):
    model = Profile

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        likes_received_count = Like.objects.filter(review__profile=self.object).count()

        context["likes_received_count"] = likes_received_count

        if self.request.user.is_authenticated:
            profile = kwargs["object"]
            context["is_profile_follow"] = profile.followers.filter(
                id=self.request.user.profile.id
            ).exists()

        return context


class ProfileUpdate(LoginRequiredMixin, View):
    template_name = "profiles/profile_form.html"

    def get(self, request):
        profile = get_object_or_404(Profile, id=request.user.profile.id)
        form = ProfileForm(instance=profile)
        ctx = {"form": form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        profile = get_object_or_404(Profile, id=request.user.profile.id)
        form = ProfileForm(request.POST, request.FILES or None, instance=profile)

        if not form.is_valid():
            ctx = {"form": form}
            return render(request, self.template_name, ctx)

        profile = form.save(commit=False)
        profile.save()

        return redirect(
            reverse("profiles:main", kwargs={"slug": self.request.user.profile.slug})
        )


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
