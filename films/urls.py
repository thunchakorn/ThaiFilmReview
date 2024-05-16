from django.urls import path

from . import views
from reviews.views import ReviewCreateView

app_name = "films"

urlpatterns = [
    path("", views.FilmListView.as_view(), name="list"),
    path("<str:slug>/", views.FilmDetailView.as_view(), name="detail"),
    path(
        "<str:slug>/review/create/",
        ReviewCreateView.as_view(),
        name="create-review",
    ),
]
