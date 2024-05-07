from django.views.generic import ListView, DetailView

from films.models import Film

class FilmListView(ListView):
    model = Film

class FilmDetailView(DetailView):
    model = Film


