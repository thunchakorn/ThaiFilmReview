from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse


def main_view(request):
    return redirect(reverse("reviews:list"))


class CriteriaView(View):
    template_name = "home/criteria.html"

    def get(self, request):
        return render(request, self.template_name)
