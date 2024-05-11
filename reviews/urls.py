from django.urls import path

from reviews.views import ReviewCreateView, ReviewDetailView, ReviewListView

app_name = "reviews"

urlpatterns = [
    path("", ReviewListView.as_view(), name="feed"),
    path("reviews/create/", ReviewCreateView.as_view(), name="create"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="detail"),
]
