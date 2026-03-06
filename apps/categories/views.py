from django.views.generic import DetailView, ListView

from apps.videos.models import Video

from .models import Topic


class TopicListView(ListView):
    model = Topic
    template_name = "categories/category_list.html"
    context_object_name = "topics"


class TopicDetailView(DetailView):
    model = Topic
    template_name = "categories/category_detail.html"
    context_object_name = "topic"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["videos"] = Video.objects.filter(is_published=True, topics=self.object).select_related("speaker", "category")
        return context
