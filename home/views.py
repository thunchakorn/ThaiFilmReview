from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse


def main_view(request):
    if request.method == "GET":
        return redirect(reverse("reviews:list"))


class CriteriaView(TemplateView):
    template_name = "home/criteria.html"
