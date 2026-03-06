from django.views.generic import DetailView, ListView

from videos.models import Video

from .models import Category


class CategoryListView(ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = (
            Video.objects.filter(visibility=Video.Visibility.PUBLISHED, categories=self.object)
            .select_related('primary_category')
            .prefetch_related('categories')
            .order_by('-is_featured', '-created_at')
        )
        return context
