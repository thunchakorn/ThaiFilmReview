from django.urls import path

from profiles import views

app_name = "profiles"

urlpatterns = [
    path("update/", views.ProfileUpdate.as_view(), name="update"),
    path("<slug:slug>/", views.ProfileDetail.as_view(), name="main"),
    path("<slug:slug>/follow/", views.ProfileFollowToggle.as_view(), name="follow"),
]
