from django.urls import path

from layout import views

app_name = "layout"

urlpatterns = [path("", views.MainView.as_view(), name="main")]
