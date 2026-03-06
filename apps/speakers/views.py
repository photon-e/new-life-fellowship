from django.views.generic import DetailView, ListView

from apps.videos.models import Video

from .models import Speaker


class SpeakerListView(ListView):
    model = Speaker
    template_name = "speakers/speaker_list.html"
    context_object_name = "speakers"


class SpeakerDetailView(DetailView):
    model = Speaker
    template_name = "speakers/speaker_detail.html"
    context_object_name = "speaker"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["videos"] = Video.objects.filter(is_published=True, speaker=self.object).select_related(
            "speaker", "category"
        )
        return context
