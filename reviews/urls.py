from django.urls import path

from reviews import views

app_name = "reviews"

urlpatterns = [
    path("", views.ReviewListView.as_view(), name="list"),
    path("create/", views.ReviewCreateView.as_view(), name="create"),
    path("<int:pk>/", views.ReviewDetailView.as_view(), name="detail"),
    path("<int:pk>/like/", views.LikeReview.as_view(), name="like-toggle"),
    path(
        "<int:pk>/comment/create/", views.CommentReview.as_view(), name="create-comment"
    ),
]
