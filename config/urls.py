from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("no-enter/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("allauth.socialaccount.urls")),
    # path("i18n/", include("django.conf.urls.i18n")),
]

# API URLS
urlpatterns += [
    path("api/", include("config.api_router")),  # API base url
    path("api/auth-token/", obtain_auth_token),  # DRF auth token
]

urlpatterns += i18n_patterns(
    path("", include("tfr.urls")),
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
