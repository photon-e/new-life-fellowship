from django.urls import path

from .views import SpeakerDetailView, SpeakerListView

app_name = "speakers"

urlpatterns = [
    path("", SpeakerListView.as_view(), name="list"),
    path("<slug:slug>/", SpeakerDetailView.as_view(), name="detail"),
]
