from django.db.models import Count
from django.views.generic import DetailView, ListView, TemplateView

from categories.models import Category

from .models import Video


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published_videos = Video.objects.filter(visibility=Video.Visibility.PUBLISHED).select_related(
            'primary_category'
        ).prefetch_related('categories')

        context['featured_videos'] = published_videos.filter(is_featured=True)[:6]
        context['latest_videos'] = published_videos[:8]
        context['categories'] = Category.objects.annotate(video_count=Count('videos')).filter(video_count__gt=0)[:8]
        return context


class VideoListView(ListView):
    model = Video
    template_name = 'videos/video_list.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_queryset(self):
        return (
            Video.objects.filter(visibility=Video.Visibility.PUBLISHED)
            .select_related('primary_category')
            .prefetch_related('categories')
        )


class VideoDetailView(DetailView):
    model = Video
    template_name = 'videos/video_detail.html'
    context_object_name = 'video'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return (
            Video.objects.filter(visibility=Video.Visibility.PUBLISHED)
            .select_related('primary_category')
            .prefetch_related('categories')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related = Video.objects.filter(visibility=Video.Visibility.PUBLISHED).exclude(pk=self.object.pk)

        if self.object.primary_category_id:
            related = related.filter(categories=self.object.primary_category)

        context['related_videos'] = related.select_related('primary_category').prefetch_related('categories')[:6]
        return context
