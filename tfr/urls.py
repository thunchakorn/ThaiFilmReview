from django.urls import path

from . import views

app_name = "tfr"

urlpatterns = [
    path("", views.MainView.as_view(), name="main"),
    path("criteria/", views.CriteriaView.as_view(), name="criteria"),
]
