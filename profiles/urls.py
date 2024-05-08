from django.urls import path

from profiles import views

app_name = "profiles"

urlpatterns = [path("<int:pk>/", views.ProfileDetail.as_view(), name="main")]
