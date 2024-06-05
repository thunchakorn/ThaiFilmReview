from django.urls import include, path

from reviews import views

app_name = "reviews"

urlpatterns = [
    path("", views.ReviewListView.as_view(), name="list"),
    path(
        "create/<str:slug>/",
        views.ReviewCreateView.as_view(),
        name="create",
    ),
    path(
        "<uuid:pk>/",
        include(
            [
                path("", views.ReviewDetailView.as_view(), name="detail"),
                path("delete/", views.ReviewDeleteView.as_view(), name="delete"),
                path("update/", views.ReviewUpdateView.as_view(), name="update"),
                path(
                    "update/spoiler/",
                    views.MarkSpoilerReviewView.as_view(),
                    name="spoiler",
                ),
                path("like/", views.LikeReview.as_view(), name="like-toggle"),
                path(
                    "comment/create/",
                    views.CommentReview.as_view(),
                    name="create-comment",
                ),
            ]
        ),
    ),
]
