from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'visibility', 'primary_category', 'is_featured', 'created_at')
    list_filter = ('visibility', 'is_featured', 'categories')
    search_fields = ('title', 'description', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
