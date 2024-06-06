from rest_framework.routers import DefaultRouter

from films.api.views import FilmViewSet

router = DefaultRouter()

router.register(r"films", FilmViewSet)


urlpatterns = router.urls
