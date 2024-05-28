from django.urls import path

from reviews import views

app_name = "reviews"

urlpatterns = [
    path("", views.ReviewListView.as_view(), name="list"),
    path(
        "create/<str:slug>/",
        views.ReviewCreateView.as_view(),
        name="create",
    ),
    path("<uuid:pk>/", views.ReviewDetailView.as_view(), name="detail"),
    path("<uuid:pk>/delete/", views.ReviewDeleteView.as_view(), name="delete"),
    path("<uuid:pk>/update/", views.ReviewUpdateView.as_view(), name="update"),
    path("<uuid:pk>/like/", views.LikeReview.as_view(), name="like-toggle"),
    path(
        "<uuid:pk>/comment/create/",
        views.CommentReview.as_view(),
        name="create-comment",
    ),
]
