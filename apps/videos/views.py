from django.db.models import Count, Q
from django.views.generic import DetailView, ListView, TemplateView

from apps.categories.models import Category, Topic
from apps.live.models import LiveStream
from apps.speakers.models import Speaker

from .models import Video


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        videos = Video.objects.filter(is_published=True).select_related("speaker", "category").prefetch_related("topics")

        context["hero_video"] = videos.filter(is_featured=True).first() or videos.first()
        context["featured_videos"] = videos.filter(is_featured=True)[:8]
        context["latest_videos"] = videos[:12]
        context["featured_speakers"] = Speaker.objects.annotate(video_count=Count("videos")).filter(video_count__gt=0)[:6]
        context["categories"] = Category.objects.annotate(video_count=Count("videos")).filter(video_count__gt=0)[:8]
        context["topics"] = Topic.objects.annotate(video_count=Count("videos")).filter(video_count__gt=0)[:8]
        context["live_stream"] = LiveStream.objects.filter(is_active=True).first()
        return context


class VideoListView(ListView):
    model = Video
    template_name = "videos/video_list.html"
    context_object_name = "videos"
    paginate_by = 12

    def get_queryset(self):
        queryset = Video.objects.filter(is_published=True).select_related("speaker", "category").prefetch_related("topics")
        category_slug = self.request.GET.get("category")
        topic_slug = self.request.GET.get("topic")

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if topic_slug:
            queryset = queryset.filter(topics__slug=topic_slug)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["topics"] = Topic.objects.all()
        context["selected_category"] = self.request.GET.get("category", "")
        context["selected_topic"] = self.request.GET.get("topic", "")
        return context


class VideoDetailView(DetailView):
    model = Video
    template_name = "videos/video_detail.html"
    context_object_name = "video"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Video.objects.filter(is_published=True).select_related("speaker", "category").prefetch_related("topics")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related = Video.objects.filter(is_published=True).exclude(pk=self.object.pk)

        related = related.filter(
            Q(category=self.object.category)
            | Q(speaker=self.object.speaker)
            | Q(topics__in=self.object.topics.all())
        ).distinct()

        context["related_videos"] = related.select_related("speaker", "category").prefetch_related("topics")[:8]
        return context
