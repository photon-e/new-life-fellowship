from django.urls import path

from .views import TopicDetailView, TopicListView

app_name = "categories"

urlpatterns = [
    path("", TopicListView.as_view(), name="topic_list"),
    path("<slug:slug>/", TopicDetailView.as_view(), name="topic_detail"),
]
