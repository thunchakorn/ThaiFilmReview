from django.urls import path

from . import views

app_name = 'films'

urlpatterns = [
    path('', views.FilmListView.as_view(), name='list')
]
