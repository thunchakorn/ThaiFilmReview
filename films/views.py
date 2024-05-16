from typing import Any
from django.db.models import Count, Avg, Exists, OuterRef
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView

from films.models import Film
from films.filters import FilmFilter


class FilmListView(ListView):
    model = Film
    paginate_by = 2
    ordering = ["-release_date", "name"]
    context_object_name = "film_list"

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.annotate(
            reviews_count=Count("reviews"), average_rating=Avg("reviews__rating")
        )
        self.filterset = FilmFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.filterset.form
        print(context["film_list"])
        return context


class FilmDetailView(DetailView):
    model = Film

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.annotate(
            reviews_count=Count("reviews"), average_rating=Avg("reviews__rating")
        )

        if self.request.user.is_authenticated:
            qs = qs.annotate(
                is_user_review=Exists(
                    Film.objects.filter(
                        id=OuterRef("id"), reviews__profile=self.request.user.profile
                    )
                )
            )

        return qs
