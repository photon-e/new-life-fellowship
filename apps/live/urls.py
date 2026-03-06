from django.urls import path

from .views import LiveView

app_name = "live"

urlpatterns = [
    path("", LiveView.as_view(), name="index"),
]
