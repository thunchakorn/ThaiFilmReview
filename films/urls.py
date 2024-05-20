from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from reviews.views import ReviewCreateView

router = DefaultRouter()
router.register(
    r"",
    views.FilmViewSet,
)

app_name = "films"


urlpatterns = [
    path("", views.FilmListView.as_view(), name="list"),
    path("api/", include(router.urls)),
    path("<str:slug>/", views.FilmDetailView.as_view(), name="detail"),
    path(
        "<str:slug>/review/create/",
        ReviewCreateView.as_view(),
        name="create-review",
    ),
]
