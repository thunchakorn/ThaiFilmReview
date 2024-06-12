from django.views.generic import TemplateView, RedirectView


class MainView(RedirectView):
    permanent = True
    pattern_name = "reviews:list"


class CriteriaView(TemplateView):
    template_name = "pages/criteria_{language_code}.html"

    def get_template_names(self) -> list[str]:
        t = self.template_name.format(language_code=self.request.LANGUAGE_CODE)
        return [t]
