from django.views.generic import ListView

from films.models import Film

class FilmListView(ListView):
    model = Film


