from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

from rest_framework.routers import DefaultRouter

from films.urls import router as FilmRouter

router = DefaultRouter()
router.registry.extend(FilmRouter.registry)

urlpatterns = [
    path("no-enter/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("api/", include(router.urls)),
    # path("i18n/", include("django.conf.urls.i18n")),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path("", include("django.contrib.auth.urls")),
]

urlpatterns += i18n_patterns(
    path("", include("home.urls")),
    path("reviews/", include("reviews.urls")),
    path("films/", include("films.urls")),
    path("profiles/", include("profiles.urls")),
)


if settings.DEBUG:
    print("DEBUG MODE".center(100, "-"))

    import debug_toolbar

    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
