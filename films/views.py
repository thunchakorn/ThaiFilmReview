from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView

from films.models import Film
from films.filters import FilmFilter

class FilmListView(ListView):
    model = Film
    paginate_by = 1
    ordering = ['-release_date', 'name']

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        self.filterset = FilmFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context

class FilmDetailView(DetailView):
    model = Film


