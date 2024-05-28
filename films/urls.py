from django.urls import path
from rest_framework.routers import DefaultRouter

from films import views

router = DefaultRouter()
router.register(r"films", views.FilmViewSet)

app_name = "films"

urlpatterns = [
    path("", views.FilmListView.as_view(), name="list"),
    path("<str:slug>/", views.FilmDetailView.as_view(), name="detail"),
]
