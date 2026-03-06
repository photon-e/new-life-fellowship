from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "speaker", "category", "duration", "is_featured", "is_published", "created_at")
    list_filter = ("is_featured", "is_published", "category", "topics")
    search_fields = ("title", "description", "slug", "speaker__name")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("speaker", "category")
    filter_horizontal = ("topics",)
