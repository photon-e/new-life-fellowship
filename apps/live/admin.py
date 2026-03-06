from django.contrib import admin

from .models import LiveStream


@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ("title", "current_program", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title", "current_program", "description")
