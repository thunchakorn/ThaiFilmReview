from django.views.generic import TemplateView, RedirectView


class MainView(RedirectView):
    permanent = True
    pattern_name = "reviews:list"


class CriteriaView(TemplateView):
    template_name = "home/criteria.html"
