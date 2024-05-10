from django.urls import path

from reviews.views import ReviewCreateView, ReviewDetailView, ReviewListView

app_name = "reviews"

urlpatterns = [
    path("", ReviewListView.as_view(), name="home"),
    path("create/", ReviewCreateView.as_view(), name="create"),
    path("<int:pk>/", ReviewDetailView.as_view(), name="detail"),
]
