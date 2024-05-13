from django.shortcuts import render
from django.views.generic import TemplateView, View


class MainView(TemplateView):
    template_name = "home/main.html"


class CriteriaView(View):
    template_name = "home/criteria.html"
    # TODO: Cache this html because it always static

    def get(self, request):
        return render(request, self.template_name)
